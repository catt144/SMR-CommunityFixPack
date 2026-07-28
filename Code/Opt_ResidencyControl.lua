-- D03 — OPTIONAL module, OFF BY DEFAULT. Not a bug fix.
--
-- Enable it by setting, before this mod loads (console on the main menu, or a
-- tiny mod that loads first):
--     SMRFixPack_Optional = { ResidencyControl = true }
-- `SMRFixPack.ListFixes()` reports it as inactive with the reason until you do.
--
-- Why it exists: the community's long-standing ask — stop new residents from
-- moving into a dome while its CURRENT residents keep commuting and using
-- services normally. The shipped game offers only blunt instruments: the
-- accept-colonists toggle is a QUARANTINE by design ("Colonists are not allowed
-- to enter or leave", T365/T7660; enforced with the literal comment
-- "quarantine, no one enters or leaves", Colonist.lua:2632-2634) and scripted
-- content depends on that seal (Wildfire's dome-local spread, TheRogueDome's
-- forced quarantine — the F61 entry records the survey; the pack's earlier F61
-- "fix" subverted it and was deleted for exactly that reason). The trait filter
-- is indirect and REMOVES a quarantine when set. This module adds the missing
-- middle setting as a new per-dome policy, leaving quarantine untouched.
--
-- WHAT THIS SHIPS: a per-dome / per-habitat "closed to new residents" policy.
--
--   * A new toggle row on the dome and MicroG-habitat infopanels (left-click
--     toggles, Ctrl+click broadcasts to all domes — the shipped
--     Community:TogglePolicy/SetPolicyState machinery, Community.lua:77-100,
--     which also plays the policy FX and respects the rogue-dome UI lock).
--   * Voluntary resettlement: post-wrapper on Community:CanAcceptNewColonists
--     (Community.lua:61-63) — a closed dome stops being offered to colonists
--     looking to move (its only caller is Colonist:FindEmigrationDome's
--     candidate filter, Colonist.lua:2658 — verified the only caller in Src).
--   * Arrivals choosing a FIRST home: post-wrapper on the global ChooseDome
--     (_GameUtils.lua:426-446) filtering closed domes out of the candidate
--     list. ChooseDome is the single choose-a-new-home funnel: rocket
--     disembark/arrivals (RocketBase.lua:1985/:2068/:2105), lander/transporter
--     arrivals (CargoTransporterNew.lua:907/:951/:975), factory-born androids
--     (DroneFactory.lua:224) and stranded colonists re-homing
--     (Colonist.lua:1149). Deliberately NOT filtered there:
--       - the `safety_dome` argument — the last-resort dome for a colonist
--         stranded outside stays available, so the policy can never suffocate
--         anyone;
--       - tourists (traits.Tourist) — they take hotel rooms, not residency in
--         the community sense, and the spec leaves hotel-seeking alone.
--   * Untouched by design: MANUAL relocation (the player's own order overrides
--     the policy), births (in-dome), homeless within their own dome (not a
--     move-in), quarantine and both passage-use toggles (fully independent).
--
-- The home-side commute gates (Dome:GetService/ChooseTraining/ChooseWorkplace,
-- ShiftsBuilding:CanWorkTrainHereDomeCheck) never read this flag, so a closed
-- dome's residents keep working, shopping and training through passages —
-- which is the whole point.
--
-- Savegame footprint (FIX_POLICY §3): `SMRFixPack_closed_to_new_residents` on
-- the Dome/Habitat object (true/false), absent-tolerant both ways — nil means
-- vanilla behavior, the unmodded game never reads it, and a save carrying the
-- flag loads fine with the module (or the pack) removed.

SMRFixPack_Optional = rawget(_G, "SMRFixPack_Optional") or {}

local FLAG = "SMRFixPack_closed_to_new_residents"

local function is_closed(dome)
	return type(dome) == "table" and dome[FLAG] and true or false
end

-- One infopanel row, cloned from the shipped accept-colonists row pattern
-- (Lua\XDef\sectionDome.generated.lua:177-217): InfopanelActiveSection with
-- everything set in OnContextUpdate. Yellow/limit styling on the closed state
-- so it cannot be mistaken for the red quarantine row above it.
local function append_policy_row(section, context)
	InfopanelActiveSection:new({
		OnContextUpdate = function(self, context, ...)
			local dome = ResolvePropObj(context)
			local closed = is_closed(dome)
			if closed then
				self:SetIcon("UI/IconsRemaster/Sections/accept_colonists_off.png")
				self:SetIconBack("UI/IconsRemaster/Sections/ip_sections_limit")
				self:SetTitle(Untranslated("Closed to new residents"))
				self:SetRolloverImageColor("yellow", true)
			else
				self:SetIcon("UI/IconsRemaster/Sections/accept_colonists_on.png")
				self:SetIconBack("UI/IconsRemaster/Sections/ip_sections_on.png")
				self:SetTitle(Untranslated("Accepts new residents"))
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
			-- rollover
			self:SetRolloverTitle(Untranslated("Residency Policy (Community Fix Pack)"))
			self:SetRolloverText(Untranslated(closed
				and "No new Colonists will move in — voluntarily or on arrival. Current residents keep commuting, working and using services through Passages exactly as before. You can still relocate Colonists here manually, and Tourists still check in.<newline><newline>Current status: <em>Closed to new residents</em>"
				or  "Close this Dome to new residents without quarantining it: no one new moves in, while current residents keep commuting, working and using services through Passages. Manual relocation and Tourists are unaffected.<newline><newline>Current status: <em>Accepts new residents</em>"))
			if closed then
				self:SetRolloverHint(Untranslated("<left_click> Accept new residents in this Dome<newline><em>Ctrl + <left_click></em> Accept new residents in all Domes"))
				self:SetRolloverHintGamepad(Untranslated("<ButtonA> Accept new residents in this Dome<newline><ButtonY> Accept new residents in all Domes"))
			else
				self:SetRolloverHint(Untranslated("<left_click> Close this Dome to new residents<newline><em>Ctrl + <left_click></em> Close all Domes to new residents"))
				self:SetRolloverHintGamepad(Untranslated("<ButtonA> Close this Dome to new residents<newline><ButtonY> Close all Domes to new residents"))
			end
		end,
	}, section, context)
end

SMRFixPack.Register("ResidencyControl", {
	title = 'OPTIONAL: per-dome "closed to new residents" policy — no quarantine involved',
	apply = function()
		if not SMRFixPack_Optional.ResidencyControl then
			return "opt-in module, off by default — set SMRFixPack_Optional = { ResidencyControl = true } before this mod loads"
		end

		local C = rawget(_G, "Community")
		if type(C) ~= "table" or type(C.CanAcceptNewColonists) ~= "function"
				or type(C.TogglePolicy) ~= "function" then
			return "Community.CanAcceptNewColonists/TogglePolicy not found (game update changed it?)"
		end
		if type(rawget(_G, "ChooseDome")) ~= "function" then
			return "ChooseDome not found (game update changed it?)"
		end
		-- Both section classes declare Init themselves (generated XDef classes),
		-- so the classdef lookup is valid at mod-load time.
		local SD = rawget(_G, "sectionDome")
		local SM = rawget(_G, "sectionMicroGHabitat")
		if type(SD) ~= "table" or type(SD.Init) ~= "function"
				or type(SM) ~= "table" or type(SM.Init) ~= "function" then
			return "sectionDome/sectionMicroGHabitat Init not found (game update changed the infopanel?)"
		end

		-- gate 1: voluntary resettlement (FindEmigrationDome's candidate filter)
		local orig_can = C.CanAcceptNewColonists
		function C:CanAcceptNewColonists(...)
			if self[FLAG] then
				return false
			end
			return orig_can(self, ...)
		end

		-- gate 2: arrivals / first-home choice. Filter the candidate list only;
		-- safety_dome passes through untouched (last-resort survival), and
		-- tourists keep the vanilla choice.
		local orig_choose = ChooseDome
		local function choose(traits, domes, safety_dome, dome_elevators, ...)
			if type(domes) == "table" and not (traits and traits.Tourist) then
				local filtered
				for i, dome in ipairs(domes) do
					if is_closed(dome) then
						if not filtered then
							filtered = {}
							for j = 1, i - 1 do
								filtered[#filtered + 1] = domes[j]
							end
						end
					elseif filtered then
						filtered[#filtered + 1] = dome
					end
				end
				domes = filtered or domes
			end
			return orig_choose(traits, domes, safety_dome, dome_elevators, ...)
		end
		_G.ChooseDome = choose
		if rawget(_G, "ChooseDome") ~= choose then
			return "could not install the ChooseDome wrapper (sandbox change?)"
		end

		-- UI: append the policy row after the shipped rows (VList order)
		local orig_sd_init = SD.Init
		function SD:Init(parent, context)
			local r = orig_sd_init(self, parent, context)
			if IsContextOfKind(context, "Dome") then
				pcall(append_policy_row, self, context)
			end
			return r
		end
		local orig_sm_init = SM.Init
		function SM:Init(parent, context)
			local r = orig_sm_init(self, parent, context)
			if IsContextOfKind(context, "MicroGHabitatBase") then
				pcall(append_policy_row, self, context)
			end
			return r
		end
	end,
})
