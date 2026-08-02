-- F57: the drone/transport minors bundle. Three items were tracked; each was
-- screened against the shipped source. Two are fixed here; the third is
-- deliberately left alone, on the grounds set out under (c) below.
-- (This line used to say "because fixing it would undo F61" — that reason was
-- withdrawn by the QA audit of 2026-07-25 and corrected under (c), but the
-- summary above it kept repeating it until 2026-08-02.)
--
---- (b) a passability change corrupts every drone's unreachables table -------
-- `OnMsg.OnPassabilityChanged` (Lua\Units\Drone.lua:851-864) drops the entries
-- belonging to the changed map by building a fresh table and swapping it in:
--     local unreachable = {}
--     for key, value in pairs(drone.unreachable_buildings) do ... end
--     drone.unreachable_buildings = unreachable
-- Two things are lost in that swap.
--
-- 1. **The weak-keys metatable.** Every other place this table is created uses
--    `setmetatable({version = g_DroneUnreachablesVersion}, weak_keys_meta)` —
--    `Drone:ApproachWrapper` (:826) and `Drone:ResetUnreachablesTable` (:875).
--    The replacement is a plain `{}`, so from the first passability change
--    onwards each drone holds a STRONG reference to every building it could not
--    reach. Salvaged and destroyed buildings are then kept alive by the drone
--    that once failed to reach them, and they keep coming back out of `pairs`
--    in `CleanUnreachables` (:890) and the recharger scan (:1281).
-- 2. **The count.** `unreachable_buildings_count` is never recomputed, so it
--    keeps the pre-change value while the table it describes has shrunk. That
--    number is not decoration: `Drone:ApproachWrapper` compares it against
--    `const.MaxUnreachablesInTable` and starts evicting the oldest entry when it
--    looks full (:827-838), and `DroneControl` only restarts its idle clock
--    while `self.unreachable_buildings_count <= 0` (:630). `CleanUnreachables`
--    then decrements the same stale number (:893) and can drive it negative.
--
-- This is NOT the nil-iteration kind of claim (the F10 lesson): the table can be
-- `false` here and this engine tolerates `pairs(false)` — no crash is asserted,
-- and none is fixed. What is fixed is the state left behind.
--
-- Patch approach: an additional `OnMsg.OnPassabilityChanged` handler
-- (FIX_POLICY §1.2 — OnMsg is additive; the shipped handler keeps running
-- untouched and ours runs after it, because mod code registers later). It
-- re-applies `weak_keys_meta` to whatever table each drone now has and
-- recomputes the count with `table.count`, which is exactly how
-- `ApproachWrapper` recomputes it after it changes the table (:841). Nothing
-- else is touched: the map filtering, the `version` key and the shipped expiry
-- all stay as they are.
--
---- (a) a non-"Fuel" rocket leaves a stale request restrictor ----------------
-- `DroneControl:UpdateRocketsInternal` (Lua\Buildings\DroneControl.lua:613-639)
-- clears exactly one key before rebuilding:
--     local r_t = self.restrictor_tables[rfRestrictorRocket]
--     r_t.Fuel = nil
-- The legacy `RocketBase` branch then writes `r_t["Fuel"]`, matching the clear.
-- The Relaunched `UniversalRocketBase` branch instead writes
-- `r_t[r.FuelResource]` (:634) — a per-class property. Whenever that is
-- anything other than the literal "Fuel", the entry it wrote is never cleared
-- again, and a request belonging to a rocket that has since left, launched or
-- been destroyed keeps restricting drone work forever.
--
-- **Latent as the game ships.** `FuelResource` is a building-template property
-- with no assignment anywhere in `ModTools\Src` (only `FuelResourceAmount` is
-- set per template), and the legacy branch hardcoding "Fuel" says what the
-- normal value is — so on shipped data the two keys coincide and nothing goes
-- wrong. Tier **R3 — latent by DATA**, not mod-only: a new rocket template with
-- its own fuel resource is a patch or a DLC away, so §4a case 3 applies and the
-- fix is in scope.
--
-- Patch approach: FIX_POLICY §1.4 chained PRE-wrapper. A wrapper cannot see
-- which key `orig` wrote — but it does not need to. It clears the WHOLE
-- restrictor table before delegating, which is what the shipped `r_t.Fuel = nil`
-- was trying to express, and vanilla then re-clears `.Fuel` and rebuilds from
-- `serviced_rockets` exactly as it always did.
-- Safe because that table has exactly one writer: created empty at
-- `DroneControl:InitRocketRestrictors` (`:174-178`), written ONLY by
-- `UpdateRocketsInternal` (`:614-637`), read by `Drone.lua:1209-1210` and the C
-- matcher (`_TaskRequest.lua:57, :75`). Nothing else parks a key there to lose,
-- and the clear and the rebuild are one synchronous call — the sole caller is
-- the restrictor thread body (`:562-574`), which cannot re-enter between them.
-- Layer: §3a **layer 2** — all work before `return orig(self)`, nothing after.
--
-- ⭐ CONVERTED 2026-08-02 from a §1.5 full replacement, on an explicit owner
-- decision (BUGS F57, "PACKAGE 0 — DECIDED: CONVERT"). FIX_POLICY §4's amended
-- R3 line allows an R3 defect to ship only as a §1.1-§1.4 patch unless the owner
-- decides otherwise; with this and F29 converted the pack holds **zero** R3 §1.5
-- replacements, so the rule is satisfied by construction rather than by
-- exception. THE DEFECT CLAIM IS UNTOUCHED — technique only.
--
-- Before/after, and the two things that actually changed:
--   * The 27-line body copy is gone, and with it the gotcha it had to work
--     around (`rfRestrictorRocket` is a FILE-LOCAL, `DroneControl.lua:12`, so a
--     verbatim copy reading it as a global would have broken every call). The
--     constant is still captured below, because the wrapper needs it to find the
--     table — but nothing depends on reproducing the body.
--   * ⭐ **A persisted mod field leaves the save.** The replacement remembered
--     the last-written key in `self.SMRFixPack_rocket_fuel_key` on a serialised
--     DroneControl; the wrapper needs no memory at all, so the field is deleted
--     from the module — and cleared from EXISTING saves by the idempotent line
--     below, so the claim is true for saves already made, not just future ones.
-- On shipped data the two shapes select identically: only the literal "Fuel" is
-- ever written, so "clear Fuel + the remembered key" and "clear everything" leave
-- the same table. **The one real difference, stated rather than buried:** if
-- another mod deliberately parked an entry in that restrictor table, we now clear
-- it. Vanilla already clears `Fuel` there on every update, so this widens an
-- existing sweep rather than inventing one.
--
---- (c) screened, deliberately NOT fixed -------------------------------------
-- `recursive_enum_dome_workplaces` (Lua\Buildings\Dome.lua:670-680) computes
--     local can_work_here = work_or_train or (cdome == colonist.dome)
--     can_work_here = can_work_here or cdome:CanColonistsFromDifferentDomesWorkServiceTrainHere()
-- so for reason "work" or "training" the quarantine test short-circuits away,
-- although the function it skips is named for exactly those cases and is
-- commented `--quarantine` where the service path calls it (Dome.lua:2907).
-- (RATIONALE CORRECTED by the QA audit 2026-07-25: an earlier version said
-- fixing this "would undo F61" — wrong. The skipped check is on `cdome`, the
-- TARGET dome; F61 removes the HOME dome's own `accept_colonists` term and
-- deliberately KEEPS the target-side check at assignment time,
-- Fix_HomeDomeMigrationGate.lua:71/:93/:113/:142. No conflict exists.) The
-- screening outcome stands on the grounds that do hold: the enumeration only
-- produces candidates, `Workplace:IsSuitable`/`TrainingBuilding:IsSuitable`
-- re-run `CanWorkTrainHereDomeCheck` before anyone is assigned (so an
-- enumeration-time check adds only redundancy), and fixing it would need a
-- §1.5 full replacement of `GetCommutableWorkplaces` recreating the file-local
-- `recursive_enum_dome_workplaces`. Recorded on the BUGS entry; not fixed.

SMRFixPack.Register("DroneTransportMinors", {
	title = "A passability change no longer corrupts each drone's unreachable-buildings table",
	apply = function()
		local err = SMRFixPack.Require("DroneTransportMinors", {
			{ class = "Drone", method = "ApproachWrapper",
			  reason = "Drone.ApproachWrapper/CleanUnreachables not found (game update changed it?)" },
			{ class = "Drone", method = "CleanUnreachables",
			  reason = "Drone.ApproachWrapper/CleanUnreachables not found (game update changed it?)" },
			{ global = "weak_keys_meta", kind = "table" },
			{ path = { "table", "count" }, kind = "function" },
		})
		if err then return err end
		local D = Drone
		local meta = weak_keys_meta

		---- (b) ---------------------------------------------------------------
		-- Runs after the shipped handler has swapped in its plain table.
		local function repair_unreachables()
			local colony = rawget(_G, "UIColony")
			local labels = colony and colony.labels
			local repaired = 0
			for _, drone in ipairs((labels and labels.Drone) or empty_table) do
				local t = drone and drone.unreachable_buildings
				if type(t) == "table" then
					-- idempotent: re-applying the same metatable costs nothing
					setmetatable(t, meta)
					-- same recount ApproachWrapper does after it edits the table
					drone.unreachable_buildings_count = table.count(t)
					repaired = repaired + 1
				end
			end
			return repaired
		end

		SMRFixPack.DroneTransportMinors = { RepairUnreachables = repair_unreachables }

		OnMsg.OnPassabilityChanged = function()
			pcall(repair_unreachables)
		end

		---- (a) ---------------------------------------------------------------
		local DC = rawget(_G, "DroneControl")
		if type(DC) ~= "table" or type(DC.UpdateRocketsInternal) ~= "function" then
			-- (b) is installed and useful on its own; say so rather than
			-- deactivating the whole fix.
			SMRFixPack.DroneTransportMinors.rockets = "DroneControl.UpdateRocketsInternal not found"
			return
		end

		-- rfRestrictorRocket is a FILE-LOCAL in the shipped file
		-- (DroneControl.lua:12, `local rfRestrictorRocket = const.rfRestrictorRocket`),
		-- so the wrapper cannot read it as a global either. Capture the constant
		-- here; `const` is populated at mod-load time.
		local rfRestrictorRocket = const.rfRestrictorRocket
		if type(rfRestrictorRocket) ~= "number" then
			SMRFixPack.DroneTransportMinors.rockets = "const.rfRestrictorRocket not found"
			return
		end

		local orig_rockets = DC.UpdateRocketsInternal

		function DC:UpdateRocketsInternal()
			-- FIX (F57a): the UniversalRocketBase branch writes
			-- r_t[r.FuelResource], but the shipped clear only ever removes the
			-- literal "Fuel" — so any other fuel resource leaves its request
			-- restricting drone work forever. Clear the whole table, which is what
			-- that line was trying to express. Safe: this method is the table's
			-- only writer, so nothing else can lose an entry, and vanilla
			-- re-clears .Fuel and rebuilds from serviced_rockets immediately below.
			local tables = self.restrictor_tables
			local r_t = tables and tables[rfRestrictorRocket]
			if type(r_t) == "table" then
				for k in pairs(r_t) do
					r_t[k] = nil
				end
			end
			-- One-shot heal, idempotent: the §1.5 shape this replaced remembered
			-- the last-written key on the DroneControl, so a save made with that
			-- version carries the field. The wrapper needs no memory — drop it, so
			-- "the field leaves the save" is true of existing saves and not only
			-- of future ones.
			if self.SMRFixPack_rocket_fuel_key ~= nil then
				self.SMRFixPack_rocket_fuel_key = nil
			end
			return orig_rockets(self)
		end
	end,
})
