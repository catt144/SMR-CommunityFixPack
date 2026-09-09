-- F46: Trains dump cargo at stations where the player switched that resource off.
--
-- Defect: Train:UnloadAll (Lua\Units\Train.lua:783-803 on game 1.0.7.396349;
-- :779-805 on 1.1.0.403908) empties the train into whatever the current station
-- has room for:
--     local station_cap = station.demand[res]:GetTargetAmount()      -- 1.0.7
--     local unload_amnt = Min(carried, station_cap)
-- with no station:IsResourceEnabled(res) check. Switching a resource off at a
-- station only removes its demand request from task_requests
-- (UniversalStorageDepotBase:SetAcceptResource, StorageDepot.lua:641-668 on
-- 1.0.7) — the demand request object itself lives on and still reports a target
-- amount, so the unload sails through.
--
-- The cargo planner then sees stock the station is not supposed to hold and
-- treats it as "forbidden excess" that must be hauled back out
-- (Train:TransferCargo, Train.lua:868, :905-939 on 1.0.7; :873, :897-940 on
-- 1.1.0), which is the resource ping-pong players see: a train drops Waste Rock
-- at a station with Waste Rock disabled, and the next train picks it up again.
--
-- Note the loading side is already correct — both load paths check
-- dest:IsResourceEnabled (1.1.0 :917-924, :935-940), so a train only ever takes
-- on cargo bound for a station that accepts it. Cargo with nowhere to go
-- therefore means something changed mid-trip (the switch was flipped, a station
-- was demolished, the train was re-assigned).
--
-- Patch approach: full replacement of Train:UnloadAll — a copy of the shipped
-- body with one guard added, marked -- FIX. Replacement rather than a wrapper
-- because the decision is mid-loop: a pre-wrapper cannot see it and a
-- post-wrapper runs after the resources have already moved.
--
-- The guard deliberately keeps two escape hatches so a fix for ping-pong can
-- never stall a train holding undeliverable cargo:
--   * if NO station on this train's route accepts the resource, the dump is
--     allowed — the cargo has nowhere else to go and holding it would occupy
--     the hold for the rest of the game;
--   * a train on its way to be stored (is_stopping) always dumps, because it is
--     about to be refabbed and anything still aboard is destroyed with it
--     (Train.lua:85-86, :457-458 -> DestroySilent -> DoDemolish on 1.0.7).
--
-- RE-COPIED 2026-09-09 on game 1.1.0.403908 (hotfix2 link 04b, re-verification
-- row F-10, VANILLA_FIX_QA §0.5 + Reader A; owner ruling ck123 = repair). Three-way
-- diff, the archived 1.0.7 tree (C:\Dev\SMR-SrcArchive\1.0.7.396349\Src) against
-- the live 1.1.0 tree against our previous copy: our copy's non-FIX lines matched
-- 1.0.7 byte for byte, and 1.1.0 changed THREE things in this body, all carried:
--   1. the inbound-cancel loop nil-guards `dest.demand and dest.demand[res]`
--      before RequestUnassignUnit (:785-787);
--   2. the cap read is hoisted and nil-guarded —
--      `local demand = station.demand and station.demand[res]` /
--      `local station_cap = demand and demand:GetTargetAmount() or 0` (:794-795).
--      THIS is the F114 line: 1.1.0 stations list lock-hidden resources
--      (BlackCube, Seeds) as storable with NO demand request, our unguarded 1.0.7
--      copy threw on every unload, and the train never left its platform;
--   3. a BlackCube hook after the unload — `BlackCubeMystery_AdjustStored(
--      station.city, unload_amnt)` (:800-802) — carried, so the Black Cubes
--      mystery's stored count stays right with the pack on.
-- The body below is the 1.1.0 one with the F46 guard re-applied on top of (2).
-- Deliberately NOT carried: nothing from 1.1.0 is dropped.
-- One change of our OWN in the helper: `route_accepts_elsewhere` no longer reads
-- `st.task_requests`. Its stated reason ("what IsResourceEnabled reads") was true
-- of 1.0.7's UniversalStorageDepotBase and is false of 1.1.0's, where
-- IsResourceEnabled = IsStoring = `self.demand[res]` exists and is not rfSuspended
-- (MultiResourceDepot.lua:242-247). The helper now tests exactly what IsStoring
-- reads — `st.demand[res]` — plus the method's presence.
--
-- ⛔ THE PREMISE IS UNREAD, AND THIS FILE SAYS SO. On 1.1.0 SetAcceptResource no
-- longer removes the demand request; it SUSPENDS it (`req:AddFlags(rfSuspended)`,
-- MultiResourceDepot.lua:251-290) and the request stays in task_requests
-- (FoodServiceBuilding.lua:1487's comment says the same of its own depot). Whether
-- a suspended request still reports a POSITIVE GetTargetAmount() — the thing that
-- makes the shipped body dump — is C-side (GetTargetAmount has no Lua definition
-- outside ResourcePile.lua:99) and NOBODY HAS OPENED IT. The re-verification's
-- verdict is "plausibly persists". Circumstantial only: 1.1.0's own load side
-- treats stock at a disabled station as forbidden excess to haul out (:873, :897,
-- :912), i.e. vanilla expects stock to land there. The 10-second control is on the
-- checklist (a station with the resource OFF: read demand[res]:GetTargetAmount()
-- from the console). If it reads 0, the guard below is inert and harmless — the
-- cap is already 0 — and F46 was fixed by 1.1.0.
--
-- ⛔ BRANCH GUARD (FIX_POLICY §2a, checklist 118): this body is written for 1.1.0
-- and the module must DECLINE on 1.0.7, where our copy would carry a BlackCube
-- hook and nil-guards over a station class that has neither (harmless) but would
-- also be the F114 shape with the branches swapped. There is no version field to
-- read (EF-077). Two checks, both testing the thing:
--   1. THE F114 GATE, KEPT, SENSE INVERTED. The measured discriminator
--      (archive/logs/gated110_*: "the Station's depot base changed to
--      MultiResourceDepotBase") was the presence of that class, which 1.0.7 did
--      not have (this header's own 1.0.7 citations name UniversalStorageDepotBase
--      as the station's depot parent). It used to DECLINE where the class exists
--      because the body was 1.0.7's; the body is 1.1.0's now, so the same fact
--      applies where the class exists and declares IsResourceEnabled
--      (MultiResourceDepot.lua:247) and declines where it does not.
--   2. A behaviour `probe` of the SHIPPED Train.UnloadAll on a stub train at a
--      stub station that lists a resource with NO demand request — the exact
--      F114 input. The 1.1.0 body survives it (cap 0, nothing moved); the 1.0.7
--      body throws on `nil:GetTargetAmount()`. STUB CONTRACT is beside the probe.
-- Three-valued (link 03's F-1 lesson): 1.1.0 shape ⇒ apply; 1.0.7 shape (no such
-- class) ⇒ decline, correct, no update_suspect; the class exists but the body
-- does not survive a missing demand entry ⇒ decline AND update_suspect, because
-- that is a body that moved again under the 1.1.0 depot base.
--
-- ⛔ NOT tested. Nothing here has run in a game; no train has unloaded on 1.1.0
-- with this body installed, and no train has been seen leaving its platform with
-- the pack on since F114 (the 09-08 boot was menu-only). A boot log line
-- `TrainCargoDumping: applied` proves the module loaded and the probe saw the
-- 1.1.0 body — nothing more. The 1.0.7 decline is argued from the archived tree
-- and a desk harness, not from a 1.0.7 boot.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-09 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Units/Train.lua Train:UnloadAll sha256=6639265f3960c94a42ed977886129e1e3a6d847541e0fa50527f84c8162b74ca
--   (Lua/Units/Train.lua:779-805 at pin time)
-- DEFECT: Min\(carried,\s*station_cap\)
--   the unload computed from the cap alone, with no enabled-resource check between
--   the cap read and the move (FIX_POLICY §2b's own worked example: the 1.0.7
--   phrasing `station.demand[res]:GetTargetAmount()` was refactored away by 1.1.0
--   with the defect untouched, so the expression states the FAULT, not the
--   phrasing). ⚠️ KNOWN LIMIT: a vanilla fix that gates the unload elsewhere (an
--   IsResourceEnabled test before the Min, or a cap that reads 0 for a suspended
--   request) leaves this expression matching and DEFECT-GONE will NOT fire — the
--   module is watched for class (b) only, and the checklist control is the real
--   answer to "did 1.1.0 fix it"

SMRFixPack.Register("TrainCargoDumping", {
	title = "Trains stop dumping cargo at stations where that resource is switched off",
	apply = function()
		local function depot_base_is_multi()
			local B = rawget(_G, "MultiResourceDepotBase")
			return type(B) == "table" and type(B.IsResourceEnabled) == "function"
		end
		local function is_107_shape()
			-- 1.0.7 had no MultiResourceDepotBase at all, and its station's depot
			-- parent was UniversalStorageDepotBase (this file's 1.0.7 record). Both
			-- halves are required: a tree with NEITHER class is not 1.0.7, it is
			-- the game having moved again, and must not decline silently.
			return rawget(_G, "MultiResourceDepotBase") == nil
				and type(rawget(_G, "UniversalStorageDepotBase")) == "table"
		end

		-- STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3), read from
		-- the shipped 1.1.0 Train:UnloadAll (Train.lua:779-805), the only code
		-- this call reaches:
		--   * self.current_station    a stub station whose storable_resources
		--                             holds ONE probe resource and whose `demand`
		--                             table has NO entry for it — the F114 input
		--                             (a lock-hidden resource listed as storable
		--                             with no request, Station.lua:110-111 +
		--                             MultiResourceCubeVisuals.lua:372-392);
		--   * self.assigned_resources an empty table, so the cancel loop (:783-789)
		--                             runs zero times; the body then REPLACES it
		--                             (:790) — a write that lands on the stub;
		--   * self:GetStoredAmount    the stub's; records the resource asked and
		--                             returns 1, so the only thing between it and
		--                             the move is the cap;
		--   * station.demand[res]     nil ⇒ `demand` nil ⇒ station_cap 0 (:794-795)
		--                             ⇒ Min(1, 0) = 0 ⇒ the move (:797-799), the
		--                             BlackCube hook (:800-802) and RequestUnassignUnit
		--                             are never reached. Min is a CommonLua global.
		-- Synchronous: no thread, no Msg. Side-effect-free: every write lands on
		-- the stub. The verdict: the shipped body asked for the probe resource's
		-- stored amount AND moved nothing AND returned = it guards a missing
		-- demand entry = 1.1.0. The 1.0.7 body indexes `station.demand[res]`
		-- unguarded (1.0.7 :798) and throws on nil — a decline. Only the literal
		-- `true` applies (00_Core.lua, Require).
		local PROBE_RES = "SMRFixPack_probe_resource"
		local function shipped_guards_missing_demand()
			local T = rawget(_G, "Train")
			if type(T) ~= "table" or type(T.UnloadAll) ~= "function" then return false end
			local asked, moved = nil, false
			local station = {
				storable_resources = { PROBE_RES },
				demand = {},
				AddResource = function() moved = true end,
			}
			local train = {
				current_station = station,
				assigned_resources = {},
				GetStoredAmount = function(_, res) asked = res return 1 end,
				AddResource = function() moved = true end,
			}
			T.UnloadAll(train)
			return asked == PROBE_RES and not moved and type(train.assigned_resources) == "table"
		end

		local err = SMRFixPack.Require("TrainCargoDumping", {
			{ class = "Train", method = "UnloadAll" },
			-- THE F114 GATE, KEPT (ck123: re-arm ON TOP of the gate, never remove
			-- it), with its sense inverted because the body below is now the
			-- 1.1.0 one: apply where the station's depot base is
			-- MultiResourceDepotBase and it declares IsResourceEnabled
			-- (MultiResourceDepot.lua:247 — a self-declared member, so a plain
			-- index sees it before the classes are flattened); decline where it
			-- does not exist. A `test`, so a 1.0.7 decline does not mark
			-- update_suspect by itself; the third-value case is marked below.
			{ test = depot_base_is_multi,
			  reason = "the Station's depot base is not MultiResourceDepotBase — this copy of Train:UnloadAll is written for game 1.1.0 and stands down on an older body" },
			{ global = "RequestUnassignUnit" },
			-- 1.1.0-only global the carried hook calls (Mysteries/BlackCubes.lua:33).
			{ global = "BlackCubeMystery_AdjustStored" },
			-- FIX (F-10, 2026-09-09) — the branch guard (FIX_POLICY §2a), as a
			-- behaviour probe of the SHIPPED body on the F114 input. Contract above.
			{ probe = shipped_guards_missing_demand,
			  reason = "the shipped Train:UnloadAll does not survive a storable resource with no demand request — this copy is written for game 1.1.0 and stands down on a different body" },
		})
		if err then
			-- Three-valued verdict. The 1.0.7 shape is a correct decline and is
			-- NOT patch rot. Anything else that declined — the 1.1.0 depot base
			-- is present but the body does not guard a missing demand entry, or
			-- a 1.1.0-only global is gone — is a pinned body over a function that
			-- moved again, and must be named in the update report. `run_apply`
			-- clears `update_suspect` only on the ACTIVE branch (00_Core.lua), so
			-- a write before returning survives.
			if not is_107_shape() then
				local entry = SMRFixPack.fixes["TrainCargoDumping"]
				if entry then entry.update_suspect = true end
			end
			return err
		end
		local T = Train

		-- Does any OTHER station this train can reach on its current route still
		-- accept `res`? Reads the route table directly (city.train_track_routes,
		-- TrainTransport.lua:308 on 1.1.0) rather than calling
		-- ForEachStationAlongTrack, which keeps shared iteration state in a
		-- file-local table.
		local function route_accepts_elsewhere(train, station, res)
			local city = station.city
			local routes = city and city.train_track_routes
			local route = routes and train.track and routes[train.track]
			if not route then return false end
			for _, st in ipairs(route) do
				-- `demand[res]` is what 1.1.0's IsResourceEnabled (= IsStoring,
				-- MultiResourceDepot.lua:242-247) reads; testing it here keeps the
				-- query safe on anything in the route table that is not a live
				-- depot for this resource.
				if st ~= station and type(st) == "table"
					and st.demand and st.demand[res] and st.IsResourceEnabled
					and st:IsResourceEnabled(res) then
					return true
				end
			end
			return false
		end

		-- copy of Lua/Units/Train.lua:779-805 (1.1.0), one guard added
		function T:UnloadAll()
			local station = self.current_station

			-- cancel all our "inbound" assignments, we'll recreate them
			for dest, cargo_list in pairs(self.assigned_resources) do
				for res, amount in pairs(cargo_list) do
					if dest.demand and dest.demand[res] then
						RequestUnassignUnit(dest.demand[res], self, amount, false)
					end
				end
			end
			self.assigned_resources = {}

			for _, res in ipairs(station.storable_resources) do
				local carried = self:GetStoredAmount(res)
				local demand = station.demand and station.demand[res]
				local station_cap = demand and demand:GetTargetAmount() or 0
				local unload_amnt = Min(carried, station_cap)
				-- FIX (F46): respect the station's per-resource switch. Skip the
				-- unload only while somewhere else on the route would take it,
				-- and never while this train is on its way to be stored.
				if unload_amnt > 0 and not self.is_stopping
					and station.IsResourceEnabled and not station:IsResourceEnabled(res)
					and route_accepts_elsewhere(self, station, res) then
					unload_amnt = 0
				end
				if unload_amnt > 0 then
					station:AddResource(unload_amnt, res)
					self:AddResource(-unload_amnt, res)
					if res == "BlackCube" then
						BlackCubeMystery_AdjustStored(station.city, unload_amnt)
					end
				end
			end
		end
	end,
})
