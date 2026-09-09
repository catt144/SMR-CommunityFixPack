-- F70: "Edit Payload" silently refills rows from the flight-policy template.
--
-- Defect: CargoRequestNew:RetrieveRequests (Lua\CargoRequestNew.lua:179-221 on game
-- 1.0.7.396349; :194-243 on 1.1.0.403908) fills the dialog from the transporter's
-- stored requests, and then, for every row whose stored request is 0, takes the
-- amount from the flight policy's cargo template instead (1.1.0 :216-234). The
-- template is suppressed in exactly one situation — while the transporter is in
-- CmdLoad (resolve_loc_cargo_template, 1.1.0 :169-192).
--
-- Two things make that a permanent nuisance rather than a one-off convenience:
--   * every landing zeroes every request (UniversalRocketBase:CmdUnload,
--     UniversalRocket.lua:486-494 on 1.0.7, :572-579 on 1.1.0, sets
--     cargo_item.requested = 0 for all cargo), so after each trip every row is 0
--     again;
--   * the Mars->asteroid template is not small (5 Drones, 20 Metals, 5 Polymers,
--     5 MachineParts, 5 Electronics, 3 extractor prefabs —
--     Data\FlightPolicyDef.lua:93-131 on 1.0.7).
-- So a player who deliberately empties a row sees it filled back in the next time
-- they open the dialog. That is the "it loads what it wants" report.
--
-- The intent is visible in the legacy dialog, which gates the same template on
-- "this transporter has not landed yet" (LanderRocketCargoRequest.lua:116). We
-- implement the same idea for the current dialog: the template is a FIRST-USE
-- default, not a running correction. Once the player has confirmed a payload for
-- this transporter, an empty row means empty.
--
-- Patch approach: full replacement of CargoRequestNew:RetrieveRequests — a copy of
-- Lua\CargoRequestNew.lua:194-243 (shipped Src, game 1.1.0.403908) — plus the
-- file-local resolve_loc_cargo_template (:169-192), reproduced because a
-- file-local cannot be reached, with the F70 gate placed inside it (see below);
-- plus a full replacement of CargoRequestNew:Apply (:368-385) with one line added
-- on its CONFIRMED path to record that the player has spoken. Changes marked
-- -- FIX.
--
-- Savegame discipline (FIX_POLICY §3): the flag is a single boolean named
-- SMRFixPack_payload_set on the transporter, and its absence is the pre-fix
-- behaviour, so a save made with the pack and loaded without it simply gets the
-- template back.
--
-- One intentional difference from the shipped copy: its `assert(transporter, ...)`
-- is dropped. assert does not unwind in mod code (it reports and carries on), so
-- it would only print a stack from our file while the `if not transporter then
-- return end` on the next line does the real work.
--
-- RE-COPIED 2026-09-08 on game 1.1.0.403908 (hotfix2 link 04, re-verification row
-- F-6, VANILLA_FIX_QA §0.5 + Reader A). Two-sided diff, the archived 1.0.7 tree
-- (C:\Dev\SMR-SrcArchive\1.0.7.396349\Src) against the live 1.1.0 tree. The old
-- 1.0.7 copy would have reverted three 1.1.0 changes; all three are carried now:
--   1. resolve_loc_cargo_template gained a second parameter, from_destination_pick,
--      which lifts the CmdLoad suppression (:174), and a tutorial branch (:183-189)
--      that pre-fills TutorialRocket_2 from AsteroidTutorialExpectedCargo and
--      returns nothing for any other rocket while g_Tutorial is set;
--   2. RetrieveRequests reads self.prev_flight_data (set on a destination pick by
--      UniversalRocketBase:UIPickDestination, UniversalRocket.lua:3236-3244) and
--      ignores the stored cargo on that path (:215-217);
--   3. the automode branch nil-guards cargo_items[id] (:199-213).
-- Apply is now an ASYNC prompt (:368-385, PromptRocketCargoIssue) with a
-- mid-flight branch (:374-377, CmdFlyToLocation) and a CancelFlight path (:382).
-- WHERE THE GATE SITS, and why (the shapes are pinned by the QA; departures say why):
--   * the gate is `not from_destination_pick and transporter.SMRFixPack_payload_set`
--     — a destination pick is meant to re-apply the template even after the
--     player has spoken, so it is exempt;
--   * it sits INSIDE our resolve_loc_cargo_template, AFTER the g_Tutorial block,
--     so the tutorial's return precedes it and TutorialRocket_2 is still
--     pre-filled with the flag set. The old copy short-circuited the resolve call
--     itself, which would have starved the tutorial;
--   * the flag is stamped on Apply's CONFIRMED path (inside `if not res or res == 1`),
--     never on Apply entry: the old pre-wrapper set it before the prompt, so a
--     player who cancelled (CancelFlight) still lost the template thereafter. To
--     put the stamp there, Apply is a body copy now, not a wrapper. Both confirmed
--     branches stamp — mid-flight and CmdLoad — because both are the player
--     confirming a payload; the cancel branch does not.
-- Deliberately NOT carried: nothing from 1.1.0 is dropped. The 1.0.7 Apply's
-- target_spot / requested_spot handling does not exist on 1.1.0 and is not
-- reproduced — which is one reason this module must not apply on 1.0.7.
--
-- ⛔ BRANCH GUARD (FIX_POLICY §2a, checklist 118): these bodies are written for
-- 1.1.0 and the module must DECLINE on 1.0.7 (our Apply copy has no
-- requested_spot handling, so on 1.0.7 it would break destination picks
-- outright). The Require below carries a behaviour `probe`: it calls the SHIPPED
-- RetrieveRequests on a stub dialog carrying prev_flight_data and a transporter
-- with a stored request of 5, and applies only if the shipped body files 0 for
-- that row — i.e. only if the body ignores stored cargo on a destination pick,
-- which is the 1.1.0 shape (:215-217) and not the 1.0.7 one (1.0.7 :193-194 reads
-- transporter.cargo unconditionally and files 5). A throw, a 5, or nothing
-- captured all decline. The STUB CONTRACT is beside the probe.
--
-- ⛔ NOT tested. Nothing here has run in a game; the payload dialog, a destination
-- pick and the new tutorial have never been exercised on 1.1.0 with the pack on.
-- A boot log line `PayloadTemplateRefill: applied` proves the module loaded and
-- the probe read the 1.1.0 shape, nothing more.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-08 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/CargoRequestNew.lua CargoRequestNew:RetrieveRequests sha256=fab60717dacfcb59b05cf3a5254fa4e30e875d658acec5548284d4426baaeefa
--   (Lua/CargoRequestNew.lua:194-243 at pin time)
-- DEFECT: amount\s*==\s*0\s+then[\s\S]{0,160}?table\.find_value\(cargo_template
--   a row whose stored request is 0 is refilled from the template on every open;
--   a vanilla fix would gate cargo_template on the player having spoken.
--   ⚠️ KNOWN LIMIT: if vanilla gates the template inside
--   resolve_loc_cargo_template instead, this expression still matches and
--   DEFECT-GONE will NOT fire — the next pin catches that as BODY-CHANGED, which
--   is why the file-local is pinned at all
-- SRC: Lua/CargoRequestNew.lua resolve_loc_cargo_template sha256=1478600112c01469ab9b61e158778f1fd26cb3864370c9c125d56f65ec342a26
--   (Lua/CargoRequestNew.lua:169-192 at pin time). No defect line on purpose:
--   this file-local is reproduced verbatim (plus our gate), so it is pinned for
--   class (b) only; there is no shipped fault inside it to state
-- SRC: Lua/CargoRequestNew.lua CargoRequestNew:Apply sha256=38b7e0e1e719fc0a3ab1e0d9560bc2de04a8a327b5dbc69f4f3e8fc790a8df82
--   (Lua/CargoRequestNew.lua:368-385 at pin time). No defect line on purpose:
--   Apply is copied only to place the stamp on its confirmed path; its shipped
--   body is correct and is pinned for class (b) only

SMRFixPack.Register("PayloadTemplateRefill", {
	title = "Edit Payload keeps the amounts you set instead of refilling them from the flight-policy template",
	apply = function()
		local REQ_METHODS = "CargoRequestNew.RetrieveRequests/Apply not found (game update changed it?)"
		local err = SMRFixPack.Require("PayloadTemplateRefill", {
			{ class = "CargoRequestNew", method = "RetrieveRequests", reason = REQ_METHODS },
			{ class = "CargoRequestNew", method = "Apply", reason = REQ_METHODS },
			{ class = "CargoRequestNew", method = "SetRequest", reason = REQ_METHODS },
			{ class = "CargoRequestNew", method = "PromptRocketCargoIssue", reason = REQ_METHODS },
			{ class = "CargoRequestNew", method = "GetCargoList", reason = REQ_METHODS },
			{ global = "GetFlightPolicy" },
			-- FIX (99a §4, 2026-09-09) — the probe below reaches this map through
			-- GetFlightPolicy, whose whole body is `return FlightPolicies[...]`
			-- (`ClassDef-Default.generated.lua:99-101`), so a nil map THROWS inside
			-- the probe. A throw there is a legitimate but SILENT decline: F70 goes
			-- off and nothing names why. `FlightPolicies` is a preset GlobalMap
			-- (`ClassDef-Default.generated.lua:76`) built during the class/data pass,
			-- and it is present on both real boot paths today because our apply runs
			-- inside a `ReloadLua` after a full first pass — but that is a boot-ORDER
			-- dependency, not a contract. This line does not change when the module
			-- declines; it changes a silent decline into a NAMED one.
			{ global = "FlightPolicies", kind = "table",
			  reason = "FlightPolicies map not built yet (mod applied before the class/data pass, or a game update moved it)" },
			{ global = "CreateRealTimeThread" },
			{ global = "CargoType", kind = "table" },
			-- FIX (F-6, 2026-09-08) — the branch guard (FIX_POLICY §2a), as a
			-- behaviour probe of the SHIPPED RetrieveRequests on a stub.
			--
			-- STUB CONTRACT (FIX_POLICY §2a, the probe form's property 3), read from
			-- the shipped 1.1.0 RetrieveRequests (:194-243) and
			-- resolve_loc_cargo_template (:169-192), the only code this call reaches:
			--   * self.transporter        non-nil; .command ~= "CmdLoad"; .cargo holds
			--                             ONE stored request of 5 for the probe row;
			--                             :GetArrivalLocType() returns a key no
			--                             FlightPolicies entry can carry, so
			--                             GetFlightPolicy (ClassDef-Default.generated.lua:99)
			--                             yields nil, the resolve returns before the
			--                             g_Tutorial block, and the template path runs
			--                             with cargo_template = nil — the shipped body's
			--                             own everyday case (table.find returns on a nil
			--                             array, LuaExportedDocs/Global/table.lua:9-11);
			--   * self.automode = false   the manual branch;
			--   * self.prev_flight_data   truthy — the destination-pick discriminator;
			--   * self.cargo_items        ONE item of type Prefab (neither Resource nor
			--                             Drone), so neither DivRound nor the Drone alias
			--                             runs;
			--   * self.SetRequest         captures (id, amount); "silent" means no
			--                             ObjModified. self.CanRequest is only reached
			--                             with a template, which the stub never has.
			-- Synchronous: no thread, no Msg. Side-effect-free: every write lands on
			-- the stub. The verdict is the amount the shipped body files for the probe
			-- row: 0 = it ignored stored cargo on a destination pick = 1.1.0;
			-- 5 = it read the stored request = 1.0.7; anything else = UNKNOWN =
			-- decline. Only the literal `true` applies (00_Core.lua, Require).
			{ probe = function()
				local C = rawget(_G, "CargoRequestNew")
				local types = rawget(_G, "CargoType")
				if type(C) ~= "table" or type(C.RetrieveRequests) ~= "function"
						or type(types) ~= "table" or types.Prefab == nil then
					return false
				end
				local captured = {}
				local transporter = {
					command = "CmdWaitOrder",
					cargo = { SMRProbeRow = { class = "SMRProbeRow", amount = 0, requested = 5 } },
					GetArrivalLocType = function() return "SMRFixPack_probe_no_such_policy" end,
				}
				local dialog = {
					automode = false,
					transporter = transporter,
					prev_flight_data = { arrival_loc = false },
					cargo_items = {
						SMRProbeRow = { id = "SMRProbeRow", type = types.Prefab, requested = 0,
							destination_available = 0, origin_available = 0 },
					},
					SetRequest = function(_, id, amount) captured[id] = amount end,
					CanRequest = function() return true end,
				}
				C.RetrieveRequests(dialog)
				return captured.SMRProbeRow == 0
			  end,
			  reason = "the shipped Edit Payload dialog still reads stored cargo on a destination pick — this copy is written for game 1.1.0 and stands down on an older body" },
		})
		if err then return err end
		local C = CargoRequestNew

		-- copy of the file-local at CargoRequestNew.lua:169-192 (1.1.0), one gate added
		local function resolve_loc_cargo_template(transporter, from_destination_pick)
			if not transporter then
				return
			end

			if transporter.command == "CmdLoad" and not from_destination_pick then
				return
			end

			local flight_policy = GetFlightPolicy(transporter)
			if not flight_policy then
				return
			end

			if g_Tutorial then
				if transporter.custom_id == "TutorialRocket_2" then
					return AsteroidTutorialExpectedCargo
				end

				return
			end

			-- FIX (F70): the template is a first-use default. Once the player has
			-- confirmed a payload for this transporter, an empty row means empty —
			-- except on a destination pick, which 1.1.0 means to re-template even
			-- in CmdLoad. Placed AFTER the tutorial block so TutorialRocket_2 is
			-- still pre-filled with the flag set.
			if not from_destination_pick and transporter.SMRFixPack_payload_set then
				return
			end

			return flight_policy.CargoTemplate
		end

		-- copy of CargoRequestNew.lua:368-385 (1.1.0), one line added
		function C:Apply()
			CreateRealTimeThread(function(self)
				local transporter = self.transporter
				local cargo_list = self:GetCargoList()
				local res = self:PromptRocketCargoIssue(cargo_list)
				if not res or res == 1 then
					-- FIX (F70): the player has just CONFIRMED a payload for this
					-- transporter; from now on an empty row is an instruction, not a
					-- gap. Stamped here, on the confirmed path only — a cancelled
					-- prompt (CancelFlight below) leaves the template alone.
					transporter.SMRFixPack_payload_set = true
					if transporter.command == "CmdFlyToLocation" then
						-- mid-flight cargo request change
						transporter.export_above = self:GetExportCargo()
						transporter.import_below = self:GetImportCargo()
					else
						transporter:SetCommand("CmdLoad", self)
					end
				else
					transporter:CancelFlight()
				end
			end, self)
		end

		-- copy of CargoRequestNew.lua:194-243 (1.1.0); the gate lives in the
		-- resolve above, this body is otherwise verbatim minus the assert
		function C:RetrieveRequests()
			local transporter = self.transporter
			if not transporter then return end

			if self.automode then
				for id, value in pairs(transporter.import_below) do
					local cargo_item = self.cargo_items[id]
					if cargo_item then
						self:SetRequest(id, value, "silent")
						cargo_item.mode = "import"
					end
				end
				for id, value in pairs(transporter.export_above) do
					local cargo_item = self.cargo_items[id]
					if cargo_item then
						self:SetRequest(id, value, "silent")
						cargo_item.mode = "export"
					end
				end
			else
				local from_destination_pick = not not self.prev_flight_data
				local cargo_template = resolve_loc_cargo_template(transporter, from_destination_pick)
				local requests = not from_destination_pick and transporter.cargo
				for id, item in pairs(self.cargo_items) do
					local request = requests and requests[id]
					local amount = request and request.requested or 0
					if amount == 0 then
						local drone_id
						if item.type == CargoType.Drone then
							drone_id = "Drone"
						end
						local template_value = table.find_value(cargo_template, "resource", drone_id or id)
						if template_value then
							amount = Max(0, template_value.amount - item.destination_available) -- only what's left to send
							amount = template_value.fill_type == "required" and amount or Min(amount, item.origin_available)
							local _, clamped = self:CanRequest(item, amount)
							if clamped and clamped ~= amount then
								amount = clamped
							end
						end
					else
						if item.type == CargoType.Resource then
							amount = DivRound(amount, const.ResourceScale)
						end
					end
					self:SetRequest(id, amount, "silent")
				end
			end
		end
	end,
})
