-- D12 — OPTIONAL module, OFF BY DEFAULT. Not a bug fix.
--
-- Enable it in-game: Options → Mod Options → Community Fix Pack (D05; the
-- toggle takes effect immediately, both directions — every hook below consults
-- SMRFixPack.IsActive per call and passes through while off, and the infopanel
-- row stops being appended to newly opened panels). Other mods / power users
-- can pre-seed SMRFixPack_Optional = { NoHomeless = true } before this mod
-- loads. `SMRFixPack.ListFixes()` reports it as inactive until enabled.
--
-- Why it exists (BUGS.md D12, found in play 2026-07-30): a specialist dome
-- STRANDS the colonists it can never house. A nursery-only child dome was
-- observed with 68 free Child slots and 28 homeless Youths/Adults sitting in
-- it, quarantine off. The cause is a vanilla TIE, not a mod defect: the
-- shipped emigration eval explicitly permits a homeless colonist to move to a
-- dome with no free housing (Colonist.lua:2676, comment "if homeless, try
-- changing community even if doesn't have living space available"), but the
-- gate above it requires a STRICTLY better score unless home or work improves
-- (:2675, :2680-2681). With zero non-cohort free slots colony-wide
-- `better_home` is false everywhere and with unemployment saturated
-- `better_work` is false too — every candidate ties, and ties never move
-- anyone. Verified byte-verbatim against the pinned 1.0.7.396349 Src on
-- 2026-08-02; no 1.0.x pass touched it.
--
-- It also compounds: the stranded homeless push the dome over IsOverpopulated
-- (Dome.lua:1026-1035) and D07's cross-dome consider() skips
-- `community.overpopulated` (Opt_CohortHousing.lua:196), so the child dome is
-- permanently excluded as a destination and no new Children ever arrive. The
-- entry's design rationale is that draining the homeless clears the flag and
-- D07 resumes unaided. ⚠️ That unwind is NOT verified — it is the reason the
-- design was chosen, and it stays a prediction until a playtest observes it.
--
-- WHAT THIS SHIPS: a per-dome / per-habitat "no homeless residents" policy.
--
--   * A new toggle row on the dome and MicroG-habitat infopanels (left-click
--     toggles, Ctrl+click broadcasts to all domes — the shipped
--     Community:TogglePolicy/SetPolicyState machinery, Community.lua:77-100,
--     which also plays the policy FX and respects the rogue-dome UI lock).
--     Same row idiom as D03, which is the DONOR PATTERN ONLY: the two modules
--     share no gate and no code (user decision, 2026-07-30).
--   * A post-wrapper on Colonist:FindEmigrationDome (declared on Colonist,
--     Colonist.lua:2581) that supplies a destination when the shipped answer
--     was EMPTY — i.e. exactly when the tie stranded them.
--
-- ⛔ HARD CONSTRAINT 1 (the trap that killed the first design): this flag has
-- its own field and its own gate and NEVER routes through
-- Community:CanAcceptNewColonists. D03's "closed to new residents" row wraps
-- that method (Opt_ResidencyControl.lua:88-93) and D07's consider() calls it
-- (Opt_CohortHousing.lua:195), so reusing D03's gate would block the cohort
-- delivery this module exists to protect. The two controls must be able to act
-- in OPPOSITE directions on the same dome at the same time:
--
--     SMRFixPack_closed_to_new_residents (D03) off → children can still migrate in
--     SMRFixPack_no_homeless             (D12) on  → graduates are pushed out
--
-- ⛔ HARD CONSTRAINT 2: NEVER expel to the surface. This wrapper can only ever
-- return a Community drawn from the city's own Community label — it has no
-- code path that returns a position, and when nothing qualifies it returns the
-- shipped answer byte-for-byte and the colonist simply stays. A colonist put
-- outside with no dome dies (F53 territory); that failure mode is made
-- structurally impossible rather than guarded against.
--
-- THE OPEN QUESTION IN THE ENTRY IS DECIDED: the NARROW reading — push only a
-- colonist their own dome can NEVER house, i.e. no residence in it is
-- IsSuitable for them (Residence.lua:162-167 — suitability is exactly the
-- exclusive_trait test). A colonist who is merely unlucky, in a dome whose
-- ordinary housing is full, is left entirely to the shipped machinery. Three
-- reasons, and the third was found by this session's source check:
--   1. It is what the child-dome case actually needs (the entry's own note).
--   2. It never competes with ChooseResidence/CheckHomeForHomeless for an
--      ordinary bed, so the module cannot fight the shortage machinery.
--   3. ⭐ It is immune to the CAPACITY-CHURN mechanism (BUGS.md C40): a law
--      can shrink Residence.capacity colony-wide while a Ministry is down,
--      and Residence:OnModifiableValueChanged (Residence.lua:224-235) EVICTS
--      the tail residents when it does. Under the BROAD reading D12 would
--      have seen those transiently-evicted colonists as homeless and shipped
--      them out of their dome for good, converting a temporary outage into a
--      permanent migration. Under the narrow reading they are untouched —
--      ordinary housing that is suitable for them exists in the dome, it is
--      merely full for a moment.
--
-- COMPOSITION AND PRECEDENCE (all deliberate):
--   * The wrapper acts ONLY when the composed answer below it is EMPTY. That
--     makes it order-independent with respect to D07, which wraps the same
--     method: whichever installs outermost, a positive answer from the other
--     module (or from the shipped code) is never overridden. It is also
--     exactly the D12 case — the tie returns false (PickEmigrationCommunity
--     over an empty best_matches, Colonist.lua:2576).
--   * Quarantine wins absolutely: accept_colonists false means "no one enters
--     or leaves" (the shipped early-out, Colonist.lua:2632-2635) and this
--     module defers to it on both sides — a sealed source dome releases
--     nobody, and a sealed destination fails CanAcceptNewColonists.
--   * A player-forced dome (CheckForcedDome) wins over the policy.
--   * The D03 row composes automatically: a closed destination already fails
--     CanAcceptNewColonists through D03's own wrapper.
--   * Ping-pong guard: destinations carrying this same flag are never
--     considered, so two flagged domes can never trade a colonist back and
--     forth.
--   * Tourists are ignored entirely (hotel machinery, not residency).
--   * A colonist with a reserved residence is mid-move and is left alone.
--
-- Destination choice, in order: a community that (a) does not carry the flag,
-- (b) CanVisit and CanAcceptNewColonists, and (c) HAS A SUITABLE RESIDENCE AT
-- ALL for this colonist. Among those, one that can house them RIGHT NOW wins
-- over one that cannot; then the nearest. Note (c) is a suitability test, not
-- a free-space test — deliberately. In the origin scenario free non-cohort
-- slots colony-wide were ZERO, so requiring free space would have made the
-- module inert in the exact case it was built for; the shipped eval has the
-- same shape for the same reason. `community.overpopulated` is NOT filtered
-- (D07 does filter it): draining an overpopulated dome is the point, and the
-- entry names only two destination filters. The free-space preference already
-- steers away from full domes.
--
-- Savegame footprint (FIX_POLICY §3): `SMRFixPack_no_homeless` on the
-- Dome/Habitat object (true/false), absent-tolerant both ways — nil means
-- vanilla behaviour, the unmodded game never reads it, and a save carrying the
-- flag loads fine with the module (or the whole pack) removed. No threads, no
-- GameVars, no globals.

SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

local FLAG = "SMRFixPack_no_homeless"

local function module_active()
	return SMRFixPack.IsActive("NoHomeless")
end

local function is_flagged(community)
	return type(community) == "table" and community[FLAG] and true or false
end

-- Every residence a community can house colonists in: the Residence label its
-- own residences are added to (Residence:SetDome, Residence.lua:171-182) PLUS
-- the community ITSELF when it is a Residence. That second clause is the
-- MicroG habitat: MicroGHabitatBase parents both LivingBase (which parents
-- Residence, Residence.lua:462-466) and Community, and its ChooseResidence
-- returns `self` (MicroGHabitat.lua:139-148). It has no parent_dome, so its
-- Residence label is empty and a label-only test would read "this community
-- can never house anyone" and evacuate every habitat.
local function each_residence(community, fn)
	if not community then return end
	if IsKindOf(community, "Residence") then
		local r = fn(community)
		if r then return r end
	end
	local list = community.labels and community.labels.Residence or empty_table
	for _, res in ipairs(list) do
		if IsValid(res) then
			local r = fn(res)
			if r then return r end
		end
	end
end

-- Does this community contain housing this colonist could EVER occupy?
-- Suitability only (Residence:IsSuitable = the exclusive_trait test) — no
-- free-space, no working-state condition. See the header for why.
local function has_suitable_home(community, colonist)
	return each_residence(community, function(res)
		return res:IsSuitable(colonist) or nil
	end) and true or false
end

-- Could this community house them RIGHT NOW? Destination ranking only.
local function has_free_suitable_home(community, colonist)
	return each_residence(community, function(res)
		return (res:IsSuitable(colonist) and res.ui_working
			and res:GetFreeSpace() > 0) or nil
	end) and true or false
end

-- The push. Installed at FILE SCOPE (the A2 lesson, FIX_POLICY §5) so the wrap
-- is in place before class flattening and a FIRST mid-session Mod Options
-- enable works without a relaunch; guarded by the same existence check apply()
-- runs, so a missing target degrades to apply()'s reason string instead of
-- erroring at load. module_active() makes the toggle live in both directions.
do
	local C = rawget(_G, "Colonist")
	if type(C) == "table" and type(C.FindEmigrationDome) == "function"
			and type(C.IsHomeless) == "function" then
		local orig_find = C.FindEmigrationDome
		function C:FindEmigrationDome(current_dome, ...)
			local dome, mode, dist, elevator = orig_find(self, current_dome, ...)
			if not module_active() then return dome, mode, dist, elevator end
			-- only ever ADD a destination; never override one
			if dome then return dome, mode, dist, elevator end
			if not self:IsHomeless() then return dome, mode, dist, elevator end
			if IsValid(self.reserved_residence) then
				return dome, mode, dist, elevator -- mid-move
			end
			local traits = self.traits
			if traits and traits.Tourist then return dome, mode, dist, elevator end
			local my_dome = self.dome
			if not is_flagged(my_dome) then return dome, mode, dist, elevator end
			if not my_dome.accept_colonists then
				return dome, mode, dist, elevator -- quarantine: no one enters or leaves
			end
			if self:CheckForcedDome() then
				return dome, mode, dist, elevator -- player order wins
			end
			if has_suitable_home(my_dome, self) then
				-- the narrow reading: this dome CAN house them, they are just
				-- unlucky — leave them to the shipped machinery
				return dome, mode, dist, elevator
			end

			-- Candidate gathering mirrors the shipped function: this city's
			-- communities plus every elevator-linked city's
			-- (Colonist.lua:2595-2618).
			local my_city = self.city
			local pos = current_dome or IsUnitInDome(self) or self:GetNavigationPos()
			local shuttles = IsLRTransportAvailable(my_city)
			local best, best_mode, best_dist, best_elev, best_free
			local function consider(community)
				if community == my_dome or is_flagged(community) then return end
				if not community:CanVisit(self) then return end
				if not community:CanAcceptNewColonists() then return end
				if not has_suitable_home(community, self) then return end
				local source_city = community.city ~= my_city and my_city
				local with_shuttles = shuttles and not source_city
				local c_mode, c_dist, c_elev =
					FindTransportationModeToCommunity(community, pos, with_shuttles, source_city)
				if not c_mode then return end
				local free = has_free_suitable_home(community, self)
				if not best
						or (free and not best_free)
						or (free == best_free and (c_dist or 0) < (best_dist or 0)) then
					best, best_mode, best_dist, best_elev, best_free =
						community, c_mode, c_dist, c_elev, free
				end
			end
			for _, community in ipairs(my_city.labels.Community or empty_table) do
				consider(community)
			end
			local seen = { [my_city] = true }
			for _, elev in ipairs(my_city.labels.Elevator or empty_table) do
				if ValidateBuilding(elev) then
					local other_city = elev.other and elev.other.city
					if other_city and not seen[other_city] then
						seen[other_city] = true
						for _, community in ipairs(other_city.labels.Community or empty_table) do
							consider(community)
						end
					end
				end
			end
			if best then
				return best, best_mode, best_dist, best_elev
			end
			-- nowhere to send them: the shipped answer stands and they stay put
			return dome, mode, dist, elevator
		end
	end
end

-- One infopanel row, same construction as D03's (see Opt_ResidencyControl.lua
-- for the full derivation of the placement rule): InfopanelActiveSection with
-- everything set in OnContextUpdate, then moved up to sit with the shipped
-- toggle group instead of below the stat blocks. The section is a VList whose
-- children render in array order, and sectionDome:Init builds the toggle rows
-- first and the plain InfopanelSection blocks after — so a row created last is
-- moved to just before the FIRST plain InfopanelSection child. If no such
-- child exists the row simply stays at the end.
--
-- Strings are Untranslated (F98, 2026-08-02): re-using a shipped translation id
-- is a NO-OP in retail — T(id, text) returns LocIdToLightUserdata(id) and
-- discards the literal (CommonLua\Core\localization.lua:250-252). Every string
-- below is new text, so Untranslated is the correct route; nothing here appends
-- to a shipped T.
--
-- Icons: the `service_in_connected_domes_*` pair is a shipped Sections asset
-- (sectionDome.generated.lua:141-147), chosen over D03's accept_colonists pair
-- so the two pack rows are not identical at a glance. Look-check is on the
-- playtest item.
local function append_policy_row(section, context)
	local row = InfopanelActiveSection:new({
		OnContextUpdate = function(self, context, ...)
			local community = ResolvePropObj(context)
			local on = is_flagged(community)
			if on then
				self:SetIcon("UI/IconsRemaster/Sections/service_in_connected_domes_on.png")
				self:SetIconBack("UI/IconsRemaster/Sections/ip_sections_limit")
				self:SetTitle(Untranslated("No homeless residents"))
				self:SetRolloverImageColor("yellow", true)
			else
				self:SetIcon("UI/IconsRemaster/Sections/service_in_connected_domes_off.png")
				self:SetIconBack("UI/IconsRemaster/Sections/ip_sections_off")
				self:SetTitle(Untranslated("Homeless residents allowed"))
				self:SetRolloverImageColor("green", true)
			end
			rawset(self, "ProcessToggle", function(self, context, broadcast)
				local building = ResolvePropObj(context)
				-- shipped policy machinery: UI-interaction gate, FX, broadcast
				building:TogglePolicy(FLAG, broadcast)
				RebuildInfopanel(building)
			end)
			self.OnActivate = function(self, context, gamepad)
				self:ProcessToggle(context, not gamepad and IsMassUIModifierPressed())
			end
			self.OnAltActivate = function(self, context, gamepad)
				if gamepad then
					self:ProcessToggle(context, true)
				end
			end
			self:SetRolloverTitle(Untranslated("Homeless Policy (Community Fix Pack)"))
			self:SetRolloverText(Untranslated(on
				and "Colonists this Dome can never house — no residence here accepts them — move to the nearest Dome that has housing of a kind they can use. Colonists who simply have no free bed here are NOT moved. Nobody is ever put outside: if there is nowhere to send them they stay, and a quarantined Dome releases no one.<newline><newline>Current status: <em>No homeless residents</em>"
				or  "Stop this Dome from stranding Colonists it can never house — a Nursery-only Dome holding grown Youths, for example. They will move to the nearest Dome with housing of a kind they can use; Colonists who simply have no free bed here are left alone, and nobody is ever put outside.<newline><newline>Current status: <em>Homeless residents allowed</em>"))
			if on then
				self:SetRolloverHint(Untranslated("<left_click> Allow homeless residents in this Dome<newline><em>Ctrl + <left_click></em> Allow homeless residents in all Domes"))
				self:SetRolloverHintGamepad(Untranslated("<ButtonA> Allow homeless residents in this Dome<newline><ButtonY> Allow homeless residents in all Domes"))
			else
				self:SetRolloverHint(Untranslated("<left_click> Move out residents this Dome cannot house<newline><em>Ctrl + <left_click></em> Do this in all Domes"))
				self:SetRolloverHintGamepad(Untranslated("<ButtonA> Move out residents this Dome cannot house<newline><ButtonY> Do this in all Domes"))
			end
		end,
	}, section, context)

	local target
	for i, child in ipairs(section) do
		if child ~= row and IsKindOf(child, "InfopanelSection")
				and not IsKindOf(child, "InfopanelActiveSection") then
			target = i
			break
		end
	end
	local from = table.find(section, row)
	if target and from and from > target then
		table.remove(section, from)
		table.insert(section, target, row)
		section:InvalidateMeasure()
	end
end

SMRFixPack.Register("NoHomeless", {
	title = 'OPTIONAL: per-dome "no homeless residents" policy — moves out only colonists the dome cannot house',
	optional = true,
	apply = function()
		if not SMRFixPack.OptionEnabled("NoHomeless") then
			return "opt-in module, off by default — enable it in Options → Mod Options"
		end

		local err = SMRFixPack.Require("NoHomeless", {
			{ class = "Colonist", method = "FindEmigrationDome",
			  reason = "Colonist.FindEmigrationDome/IsHomeless not found (game update changed it?)" },
			{ class = "Colonist", method = "IsHomeless",
			  reason = "Colonist.FindEmigrationDome/IsHomeless not found (game update changed it?)" },
			{ class = "Colonist", method = "CheckForcedDome",
			  reason = "Colonist.CheckForcedDome not found (game update changed it?)" },
			{ class = "Residence", method = "IsSuitable",
			  reason = "Residence.IsSuitable/GetFreeSpace not found (game update changed it?)" },
			{ class = "Residence", method = "GetFreeSpace",
			  reason = "Residence.IsSuitable/GetFreeSpace not found (game update changed it?)" },
			{ class = "Community", method = "TogglePolicy",
			  reason = "Community.TogglePolicy/CanAcceptNewColonists not found (game update changed it?)" },
			{ class = "Community", method = "CanAcceptNewColonists",
			  reason = "Community.TogglePolicy/CanAcceptNewColonists not found (game update changed it?)" },
			{ global = "FindTransportationModeToCommunity",
			  reason = "emigration transport helpers not found (game update changed them?)" },
			{ global = "IsLRTransportAvailable",
			  reason = "emigration transport helpers not found (game update changed them?)" },
			{ class = "sectionDome", method = "Init",
			  reason = "sectionDome/sectionMicroGHabitat Init not found (game update changed the infopanel?)" },
			{ class = "sectionMicroGHabitat", method = "Init",
			  reason = "sectionDome/sectionMicroGHabitat Init not found (game update changed the infopanel?)" },
		})
		if err then return err end
		local SD = sectionDome
		local SM = sectionMicroGHabitat

		-- the FindEmigrationDome wrapper is installed at file scope above —
		-- see the header; apply() only validates its targets.

		local orig_sd_init = SD.Init
		function SD:Init(parent, context)
			local r = orig_sd_init(self, parent, context)
			if module_active() and IsContextOfKind(context, "Dome") then
				pcall(append_policy_row, self, context)
			end
			return r
		end
		local orig_sm_init = SM.Init
		function SM:Init(parent, context)
			local r = orig_sm_init(self, parent, context)
			if module_active() and IsContextOfKind(context, "MicroGHabitatBase") then
				pcall(append_policy_row, self, context)
			end
			return r
		end
	end,
})
