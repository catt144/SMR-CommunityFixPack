-- F70: "Edit Payload" silently refills rows from the flight-policy template.
--
-- Defect: CargoRequestNew:RetrieveRequests (Lua\CargoRequestNew.lua:179-221) fills
-- the dialog from the transporter's stored requests, and then, for every row whose
-- stored request is 0, takes the amount from the flight policy's cargo template
-- instead (:194, :199-212). The template is suppressed in exactly one situation —
-- while the transporter is in CmdLoad (resolve_loc_cargo_template, :166-177).
--
-- Two things make that a permanent nuisance rather than a one-off convenience:
--   * every landing zeroes every request (UniversalRocketBase:CmdUnload,
--     UniversalRocket.lua:486-494 sets cargo_item.requested = 0 for all cargo), so
--     after each trip every row is 0 again;
--   * the Mars->asteroid template is not small (5 Drones, 20 Metals, 5 Polymers,
--     5 MachineParts, 5 Electronics, 3 extractor prefabs —
--     Data\FlightPolicyDef.lua:93-131).
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
-- Lua\CargoRequestNew.lua:179-221 (shipped Src, 2026-07) with one line gated,
-- marked -- FIX; the file-local resolve_loc_cargo_template (:166-177) is
-- reproduced verbatim because a file-local cannot be reached. Plus a pre-wrapper
-- on CargoRequestNew:Apply — the payload-confirm path (:341-355, reached from
-- UISetPayloadRequest :414-424) — to record that the player has spoken.
--
-- Savegame discipline (FIX_POLICY §3): the flag is a single boolean named
-- SMRFixPack_payload_set on the transporter, and its absence is the pre-fix
-- behaviour, so a save made with the pack and loaded without it simply gets the
-- template back.
--
-- One intentional difference from the shipped copy: its `assert(transporter, ...)`
-- on :181 is dropped. assert does not unwind in mod code (it reports and carries
-- on, see STATUS.md), so it would only print a stack from our file while the
-- `if not transporter then return end` on the next line does the real work.

SMRFixPack.Register("PayloadTemplateRefill", {
	title = "Edit Payload keeps the amounts you set instead of refilling them from the flight-policy template",
	apply = function()
		local C = rawget(_G, "CargoRequestNew")
		if type(C) ~= "table" or type(C.RetrieveRequests) ~= "function"
			or type(C.Apply) ~= "function" or type(C.SetRequest) ~= "function" then
			return "CargoRequestNew.RetrieveRequests/Apply not found (game update changed it?)"
		end
		if type(rawget(_G, "GetFlightPolicy")) ~= "function" then
			return "GetFlightPolicy not found (game update changed it?)"
		end
		if type(rawget(_G, "CargoType")) ~= "table" then
			return "CargoType not found (game update changed it?)"
		end

		-- verbatim copy of the file-local at CargoRequestNew.lua:166-177
		local function resolve_loc_cargo_template(transporter)
			if not transporter or transporter.command == "CmdLoad" then
				return
			end

			local flight_policy = GetFlightPolicy(transporter)
			if not flight_policy then
				return
			end

			return flight_policy.CargoTemplate
		end

		local orig_apply = C.Apply
		function C:Apply(...)
			-- FIX (F70): the player has just confirmed a payload for this
			-- transporter; from now on an empty row is an instruction, not a gap.
			local transporter = self.transporter
			if transporter then
				transporter.SMRFixPack_payload_set = true
			end
			return orig_apply(self, ...)
		end

		function C:RetrieveRequests()
			local transporter = self.transporter
			if not transporter then return end

			if self.automode then
				for id, value in pairs(transporter.import_below) do
					self:SetRequest(id, value, "silent")
					self.cargo_items[id].mode = "import"
				end
				for id, value in pairs(transporter.export_above) do
					self:SetRequest(id, value, "silent")
					self.cargo_items[id].mode = "export"
				end
			else
				-- FIX (F70): the template is a first-use default. Was an
				-- unconditional resolve_loc_cargo_template(transporter).
				local cargo_template = not transporter.SMRFixPack_payload_set
					and resolve_loc_cargo_template(transporter) or nil
				local requests = transporter.cargo
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
