-- C50: SpaceY grants +20 Drone Hub command capacity and its description never
-- says so — the only sponsor in the game that hides a modifier it carries.
--
-- ⭐ NOTHING VANILLA IS RE-WORDED, AND NO NUMBER IS OURS. This module adds one
-- bullet, built out of the game's own shipped sentence and the game's own
-- computed value, to the SpaceY sponsor description only.
--
-- ── The defect ────────────────────────────────────────────────────────────
-- The SpaceY MissionSponsorPreset (Data\MissionSponsorPreset.lua:605-704) ends
-- with exactly two gameplay modifiers:
--     Effect_ModifyLabel{ Label = "Consts",   Prop = "CommandCenterMaxDrones", Amount = 20 }
--     Effect_ModifyLabel{ Label = "DroneHub", Prop = "starting_drones",        Amount =  4 }
-- and its `effect` text (:625, T(880574954148, …)) names only the second:
-- "<bullet> Drone Hubs start with additional Drones". `CommandCenterMaxDrones`
-- appears nowhere in the string and nowhere else on the preset.
-- The control is a whole-tree sweep, not an impression: 16 MissionSponsorPreset
-- blocks, 6 carry an Effect_ModifyLabel, and 5 of those 6 describe EVERY
-- modifier they carry — three of them with the exact number (agent/bugs/C50.md).
-- A paired authored change with one half missing, the C39/C47 shape.
--
-- ── ⛔ The two obvious repairs are both dead, and were killed before this file
-- (1) REPLACING `preset.effect` with corrected text is a no-op in retail that
--     costs eight languages: T(id, text) returns LocIdToLightUserdata(id) and
--     DISCARDS the literal whenever TranslationTable[id] exists
--     (CommonLua\Core\localization.lua:250-252), so a NEW id — which no shipped
--     pack contains — renders its English literal for everyone. That is EF-039,
--     and it is what made Fix_TechDescriptionBuilding a shipped no-op (F98).
-- (2) CONCATENATING onto `preset.effect` breaks the bullet above it. All three
--     render sites wrap the field as `T{sponsor.effect, context}`, and the T
--     constructor SHORT-CIRCUITS on a concatenation —
--     `if getmetatable(T[1]) == TConcatMeta then return T[1] end` (:224-227) —
--     returning it WITHOUT the context. SpaceY's first bullet resolves
--     `(<cargo>)` out of that context. Breaking bullet 1 to complete bullet 3 is
--     not a repair.
--
-- ── The route this file takes: leave the preset alone, append at the UI ────
-- `preset.effect` is never touched, so the game keeps binding its own context to
-- it and every existing bullet renders exactly as it does today. We append one
-- more element at each function that ASSEMBLES the description. ⭐ All three
-- already return a concatenation in vanilla, so adding an element is
-- structurally what that code does on every draw:
--   GetSponsorSummary          returns TList(texts, "\n")             (a TConcat)
--   GetSponsorDescr            returns key_info..header..effect..…    (a TConcat)
--   LandingSiteObject:GetMissionSponsorEffect returns start..rockets..effect
--
-- ── ⛔ THE SITE LIST WAS RE-DERIVED HERE AND IT IS NOT THE ONE ON RECORD ───
-- Enumerated this session over the whole of ModTools\Src (pinned build
-- 1.0.7.396349, EF-014 — ⚠️ `Src` is under the install dir literally named
-- `Project Spark`; the `Surviving Mars` folder's ModTools has no `Src`), by
-- grepping every read of a `.effect` field rather than the one spelling:
--
--   LIVE  GetSponsorSummary            Lua\PreGameMission.lua:574
--         1 caller — Lua\XDef\PGMissionSummaryDlg.generated.lua:116, the
--         mission summary panel. ⛔ AMENDED 2026-08-20: that PANEL has TWO
--         instantiation sites, and only one of them is pre-game —
--         PGMissionSponsorRemastered.generated.lua:609 (pre-game) and
--         MissionProfileDlgRemastered.generated.lua:342 (the IN-GAME Goals
--         dialog, Lua\X\HUD.lua:283-288). One caller, two screens. See
--         `in_running_game` for why the second one is declined.
--   LIVE  GetSponsorDescr              Lua\PreGameMission.lua:644
--         1 caller — GetSponsorEntryRollover (:700), itself called once from
--         Lua\X\XPGMission.lua:158: the rollover on the sponsor picker.
--   LIVE  LandingSiteObject:GetMissionSponsorEffect  Lua\UI\PlanetUI.lua:314
--         1 caller — the <MissionSponsorEffect> tag in
--         Lua\XDef\PGChallengeLandingSpotRemastered.generated.lua:611. Reachable:
--         three shipped Challenges set sponsor = "SpaceY" (Data\Challenge.lua).
--   ⛔ DEAD  GetMissonProfileText       Lua\MissionProfileDlg.lua:25 (the typo is
--         vanilla's). ZERO callers in all of Src — the whole-tree search for
--         `MissonProfile` returns the definition line and nothing else. The
--         in-game profile dialog is MissionProfileDlgRemastered, which opens via
--         OpenDialog (Lua\X\HUD.lua:286) and never renders sponsor.effect at all.
--         ⇒ NOT WRAPPED. Shipping code for a function with no shipped caller is
--         what FIX_POLICY §4a bars (tier R4, the F28 lesson).
-- No XDef binds an <effect> tag, so there is no fourth render path.
--
-- ── ⭐ The bullet is fully translated, and the number is the game's own ────
-- Text: translation id 4706, the ConstDef help of CommandCenterMaxDrones itself
-- ("Maximum number of Drones a Drone Hub can control", Lua\__const.lua:53). All
-- nine shipped packs under `Local\` were extracted this session with this repo's
-- tools\flpk_extract.py and their CurrentLanguage/Game.csv read directly: 4706
-- carries a real translation in all eight non-English packs (German "Maximale
-- Anzahl an Drohnen, die ein Drohnen-Hub kontrollieren kann"), and its empty
-- English Translation column is not a gap — csv_load_fields maps CSV column 2 to
-- `text` (localization.lua:920) and ProcessLoadedTables (:938-960) resolves
-- English as { translated_new, TEXT, translated }, so English resolves to the
-- English source. Because the id is ENROLLED, EF-039's mechanism works FOR us
-- here: the literal below is discarded and the shipped translation is printed.
-- ⚠️ DISCLOSURE, and it is the honest cost of getting a translated bullet at
-- all: that sentence belongs to another object. It is the const's own help text
-- rather than a line written for this sponsor. The alternative, 887279699046
-- ("Drone Hubs are able to operate additional Drones"), is the DroneHubEfficiency
-- policy's description and is less defensible — it would follow that policy's
-- wording if a patch reworded it, and it carries no number.
--
-- Number: never a literal. GetModifiedConsts walks the sponsor's own
-- Effect_ModifyLabel entries and writes t[mod.Prop] = base + Amount
-- (PreGameMission.lua:519-532), so we call it for the same sponsor the site is
-- rendering and let the <CommandCenterMaxDrones> tag resolve out of that table.
-- If a patch changes the base const, the bullet changes with it.
-- ⚠️ Like every other bullet on those screens, the value is the PRE-GAME one:
-- g_Consts still holds the base there, so the sponsor's +20 shows once.
-- ⛔ CORRECTED 2026-08-20 (link 4 preparation, owner-ruled at checklist 61):
-- this paragraph used to end "All three sites are pre-game screens" and THAT WAS
-- FALSE. Site 1's panel is rebuilt by the in-game Mission Profile dialog, where
-- g_Consts already carries the sponsor's modifier and the number would be
-- double-counted. The module now stands down while a game is running — see
-- `in_running_game` below for the full derivation. The three WRAPPERS are still
-- the three named above; it is the SCREENS that were miscounted, and the miss
-- was in the record twice before anyone looked.
--
-- Our template string contains no English of ours: "\n<bullet> <drone_cap_help>
-- (<CommandCenterMaxDrones>)" is tags and punctuation only (IsTagsAndPunctuation,
-- localization.lua:131), <bullet> being the game's own TagLookupTable entry
-- (PreGameMission.lua:572).
--
-- ── Handles, and what happens when they stop working (FIX_POLICY §2) ───────
-- Every check is re-run PER CALL, because these panels are rebuilt on every draw
-- and a mid-session language change must be able to change the answer:
--   * the sponsor must BE SpaceY (this is a repair to one preset, not a new
--     house style for all sixteen);
--   * its `effect` must still carry translation id 880574954148, read with
--     TGetID rather than assumed — the day a patch rewords or repairs it, the id
--     moves, we stand down, and the player sees vanilla;
--   * the modifier must still be there: the value GetModifiedConsts computes for
--     this sponsor must EXCEED the base const, which is the defect restated;
--   * id 4706 must be in the language table loaded right now.
-- Each site stands down independently, loudly in our log (first decline only —
-- a per-draw line would flood the file) and silently on screen.
-- ⚠️ The one thing no check can catch: an id kept but its text rewritten
-- upstream to already mention the cap. No runtime surface can see that; the
-- after-every-patch extraction diff (WORKFLOW.md) is the real re-verification.
--
-- ⚠️ GetSponsorDescr carries an extra guard the other two do not need. It prints
-- starting laws and flavour text AFTER the effect (:666-691), and we can only
-- append at the end — so appending would put the bullet below them. Today it
-- lands correctly by construction: FactionDefs.SpaceY declares no initial_laws
-- (Data\FactionDef\SpaceY.lua) and the preset has no flavor_text. Both are
-- re-checked per call, and if either ever becomes non-empty that site declines
-- rather than printing the bullet in the wrong place.
--
-- ── §3a layer statement: LAYER 3 — nothing of ours enters a save ──────────
-- ⭐ THIS MODULE WRITES NOTHING. No persisted class, no GameVar, no game-time
-- thread, no OnMsg.LoadGame, no state of any kind: it is pre-game UI text,
-- rebuilt from scratch every time a panel draws. Neither route into a savegame
-- is open to it — the wrapper bodies contain no Sleep/WaitMsg, so no frame of
-- ours can sit below a blocking call; and the only things holding our functions
-- are two entries in _G and one class table, none of which the engine persists.
-- These screens are not even reachable while a savegame exists. That is what
-- makes this fix free to add to any existing save and free to remove from one.
--
-- ── Prior art (FIX_POLICY §8) ─────────────────────────────────────────────
-- fredware's SMR Community Fixes #9, *Restore SpaceY Description*, identified
-- the omission first and states the benefit correctly. Their module takes route
-- (1) above and therefore carries the eight-language regression; the
-- localization consequence, the site enumeration and the borrowed-id
-- construction here are ours.
--
-- ⛔ UNOBSERVED. Nothing here has been seen on a screen. No leg of this project
-- has ever watched a shipped-id string render in a non-English language
-- (EF-039's own closing note), and this is not the leg that changes that.

local ID = "SpaceYDroneCapBullet"
local log = SMRFixPack.Log

local SPONSOR   = "SpaceY"
local EFFECT_ID = 880574954148   -- SpaceY's shipped `effect` string
local PROP      = "CommandCenterMaxDrones"
local HELP_ID   = 4706
local HELP_EN   = "Maximum number of Drones a Drone Hub can control"

-- Tags and punctuation only — the sentence and the number both arrive through
-- the context, so no English of ours is in this string.
local BULLET = "\n<bullet> <drone_cap_help> (<CommandCenterMaxDrones>)"

-- Counters, exposed for the TestKit probe. `reason` holds the FIRST decline at
-- each site; the panels redraw constantly and a per-call log line would flood.
-- `probe` is not a render site: it is the bucket the TestKit's wave-13 check
-- passes when it drives bullet_for directly, so a probe call can never disturb
-- the three real sites' counters (and its decline reason stays readable).
local stats = {
	summary   = { patched = 0, declined = 0, reason = "" },
	descr     = { patched = 0, declined = 0, reason = "" },
	challenge = { patched = 0, declined = 0, reason = "" },
	probe     = { patched = 0, declined = 0, reason = "" },
}

local function note_decline(site, reason)
	local s = stats[site]
	s.declined = s.declined + 1
	if s.reason == "" then
		s.reason = reason
		log("%s: %s", ID, reason)
	end
	return nil
end

local function note_patch(site)
	local s = stats[site]
	s.patched = s.patched + 1
	if s.patched == 1 then
		log("%s: %s now carries the Drone Hub capacity bullet (translation id %d)", ID, site, HELP_ID)
	end
end

-- Is this id reachable by the localization system in the language loaded RIGHT
-- NOW? Re-read per call: the player can change language mid-session and the
-- engine rebuilds the table (options.lua:885).
local function enrolled(id)
	local tt = rawget(_G, "TranslationTable")
	return type(tt) == "table" and tt[id] ~= nil
end

-- Hand the call straight back unless this repair is ours to make (FIX_POLICY §2
-- — the registry status AND the veto, re-read per call so a mid-session veto
-- works, and so a PARTIAL install below is a pass-through rather than a hazard).
-- The SMRFixPack read is the §3a orphan gate: reading a nil global is safe, so a
-- captured copy of this closure would exit here rather than part-way through.
local function inert()
	local pack = rawget(_G, "SMRFixPack")
	if type(pack) ~= "table" or not pack.IsActive(ID) then return true end
	local vetoed = rawget(_G, "SMRFixPack_Disabled")
	if type(vetoed) == "table" and vetoed[ID] then return true end
	return false
end

-- Is this the one preset this fix is about? Answered BEFORE anything is read,
-- allocated or logged, so every other sponsor's call is byte-for-byte vanilla
-- (FIX_POLICY §2, the foreign-object rule).
local function ours(sponsor)
	return type(sponsor) == "table" and sponsor.id == SPONSOR
end

---- the bullet ------------------------------------------------------------

-- ⛔ THIS BULLET CAN ONLY BE BUILT WHERE `g_Consts` STILL HOLDS THE UNMODIFIED
-- BASE, and that is pre-game only. In a running game the sponsor's own
-- Effect_ModifyLabel has ALREADY been applied to `g_Consts` — `Colony.lua:76`
-- puts `g_Consts` in the "Consts" label and `Effect_ModifyLabel:OnApplyEffect`
-- sets a Modifier on every object in that label (`MarsGameEffects.lua:161-172`)
-- — so `GetModifiedConsts`, which computes `MulDivRound(g_Consts[Prop], …) +
-- Amount` (`PreGameMission.lua:518-532`), adds the same +20 a SECOND time:
--     pre-game   base 20 → value 40   ✅ the true cap
--     in-game    base 40 → value 60   ⛔ the cap is 40; SpaceY's bonus twice
-- ⚠️ And the `value <= base` test below CANNOT catch it — it is satisfied by
-- the very double-count that causes it (60 > 40).
--
-- ⚠️ This is not hypothetical, and the site list two sessions had recorded is
-- what hid it. `PGMissionSummaryDlg` — the panel site 1 feeds — is instantiated
-- TWICE: at `PGMissionSponsorRemastered.generated.lua:609` (pre-game) and at
-- `MissionProfileDlgRemastered.generated.lua:342`, the ⛔ IN-GAME Mission
-- Profile dialog opened by the HUD's Goals button (`Lua\X\HUD.lua:283-288`).
-- Its context update calls `GetSponsorSummary(entry)` whenever `MainCity` is
-- set (`PGMissionSummaryDlg.generated.lua:108-120`), and `g_CurrentMissionParams`
-- survives the savegame (`PreGameMission.lua:316, :321`), so the running game's
-- sponsor entry is live there.
--
-- ⇒ We stand down while a game is running and the player sees vanilla on that
-- panel. `MainCity` is the game's OWN pre-game/in-game discriminator on this
-- exact panel (`:110`), which is why it is the handle used here rather than a
-- test of our own invention. Fixing the number instead of declining would mean
-- re-implementing the game's modifier arithmetic, which this module exists to
-- avoid (see the header: the number is never ours).
-- ⚖️ Owner-ruled 2026-08-20 (checklist 61) before the fix was ever observed.
local function in_running_game()
	return rawget(_G, "MainCity") and true or false
end

-- Build the missing bullet for `sponsor`, or return nil having recorded why.
local function bullet_for(sponsor, site)
	if in_running_game() then
		return note_decline(site,
			"a game is running, so the Drone Hub capacity already includes SpaceY's own bonus and this bullet would count it twice — nothing was added (this repair is for the pre-game sponsor screens)")
	end
	local id_of = rawget(_G, "TGetID")
	if type(id_of) ~= "function" then
		return note_decline(site,
			"TGetID is not available — the sponsor's description cannot be identified, so nothing was added")
	end
	if id_of(sponsor.effect) ~= EFFECT_ID then
		return note_decline(site, string.format(
			"SpaceY's description is no longer translation id %d — nothing was added (a game update reworded it, or another mod replaced it)",
			EFFECT_ID))
	end

	local modified = rawget(_G, "GetModifiedConsts")
	if type(modified) ~= "function" then
		return note_decline(site, "GetModifiedConsts is not available — the Drone Hub capacity cannot be read, so nothing was added")
	end
	-- The commander is deliberately omitted: it only reaches modifiableConsts /
	-- directlyModifiableConsts (PreGameMission.lua:469-482), and this const is in
	-- neither, so the value is identical with or without it.
	local context = modified(sponsor)
	local consts = rawget(_G, "g_Consts")
	local value = type(context) == "table" and context[PROP]
	local base  = type(consts) == "table" and consts[PROP]
	if type(value) ~= "number" or type(base) ~= "number" then
		return note_decline(site, "the Drone Hub capacity const could not be read — nothing was added")
	end
	-- The defect, restated as a test: SpaceY still raises the cap above default.
	if value <= base then
		return note_decline(site,
			"SpaceY no longer raises the Drone Hub Drone capacity above the default — nothing was added (the game changed the preset)")
	end
	if not enrolled(HELP_ID) then
		return note_decline(site, string.format(
			"translation id %d is not in this build's language table — nothing was added", HELP_ID))
	end

	context.drone_cap_help = T(HELP_ID, HELP_EN)
	return T{BULLET, context}
end

-- Append `piece` to a value the game built, refusing anything that is not a
-- localized string and containing a throw rather than taking a panel down with
-- it. Returns the joined value, or nil after recording the decline.
local function append(value, piece, site, what)
	local is_t = rawget(_G, "IsT")
	if type(is_t) == "function" and not is_t(value) then
		return note_decline(site, what .. " is not a localized string — nothing was added")
	end
	local ok, joined = pcall(function() return value .. piece end)
	if not ok then
		return note_decline(site, "appending to " .. what .. " raised and was contained: " .. tostring(joined))
	end
	return joined
end

---- site 1 — the pre-game mission summary panel ---------------------------

local function wrap_summary(orig)
	return function(sponsor, ...)
		local res = orig(sponsor, ...)
		if inert() or not ours(sponsor) then return res end
		if type(res) ~= "table" or res.text == nil then return res end
		local ok, piece = pcall(bullet_for, sponsor, "summary")
		if not ok then
			note_decline("summary", "the summary pass raised and was contained: " .. tostring(piece))
			return res
		end
		if piece then
			local joined = append(res.text, piece, "summary", "the sponsor summary text")
			if joined then
				res.text = joined
				note_patch("summary")
			end
		end
		return res
	end
end

---- site 2 — the rollover on the sponsor picker ---------------------------

-- GetSponsorDescr prints starting laws and flavour text after the effect, and we
-- can only append at the end. Today SpaceY has neither, so the end IS directly
-- after the effect; if that ever changes we decline instead of misplacing it.
local function descr_tail_is_empty(sponsor)
	local factions = rawget(_G, "FactionDefs")
	local def = sponsor.faction and type(factions) == "table" and factions[sponsor.faction]
	local laws = type(def) == "table" and def.initial_laws
	if type(laws) == "table" and next(laws) then return false end
	local flavor = sponsor.flavor_text
	if flavor and flavor ~= "" then return false end
	return true
end

local function wrap_descr(orig)
	return function(sponsor, ...)
		local res = orig(sponsor, ...)
		if inert() or not ours(sponsor) then return res end
		local ok, piece = pcall(function()
			if not descr_tail_is_empty(sponsor) then
				return note_decline("descr",
					"SpaceY now has starting laws or flavour text, which this rollover prints after the effects — the bullet would land in the wrong place, so nothing was added")
			end
			return bullet_for(sponsor, "descr")
		end)
		if not ok then
			note_decline("descr", "the rollover pass raised and was contained: " .. tostring(piece))
			return res
		end
		if piece then
			local joined = append(res, piece, "descr", "the sponsor rollover text")
			if joined then
				note_patch("descr")
				return joined
			end
		end
		return res
	end
end

---- site 3 — the challenge landing-spot screen ----------------------------

-- The method takes no argument; it resolves the selected sponsor itself
-- (PlanetUI.lua:315). Same lookup, every step guarded.
local function selected_sponsor()
	local params = rawget(_G, "MissionParams")
	local current = rawget(_G, "g_CurrentMissionParams")
	local find = type(table) == "table" and table.find_value
	if type(params) ~= "table" or type(current) ~= "table" or type(find) ~= "function" then return end
	local slot = params.idMissionSponsor
	if type(slot) ~= "table" or type(slot.items) ~= "table" then return end
	return find(slot.items, "id", current.idMissionSponsor)
end

local function wrap_challenge(orig)
	return function(self, ...)
		local res = orig(self, ...)
		if inert() then return res end
		local ok, piece = pcall(function()
			local sponsor = selected_sponsor()
			if not ours(sponsor) then return nil end
			return bullet_for(sponsor, "challenge")
		end)
		if not ok then
			note_decline("challenge", "the challenge pass raised and was contained: " .. tostring(piece))
			return res
		end
		if piece then
			local joined = append(res, piece, "challenge", "the challenge sponsor effect text")
			if joined then
				note_patch("challenge")
				return joined
			end
		end
		return res
	end
end

---- install ---------------------------------------------------------------

local installed = false

SMRFixPack.Register(ID, {
	title = "SpaceY grants +20 Drone Hub Drone capacity and never mentions it — its sponsor description now carries that bullet, in the game's own words and with the game's own number",
	apply = function()
		local err = SMRFixPack.Require(ID, {
			{ global = "T" },
			{ global = "TGetID" },
			{ global = "IsT" },
			{ global = "TranslationTable", kind = "table" },
			{ global = "GetSponsorSummary" },
			{ global = "GetSponsorDescr" },
			{ global = "GetModifiedConsts" },
			{ global = "g_Consts", kind = "any" },
			{ class = "LandingSiteObject", method = "GetMissionSponsorEffect" },
			-- A content check, not a shape check: it says the remedy still
			-- exists. Require does not mark `test` failures as patch rot, which
			-- is right — a missing language record is not a game-update suspect.
			{ test = function() return enrolled(HELP_ID) end,
				reason = "this build's language pack does not carry the Drone Hub capacity record — there is no translated sentence to borrow" },
		})
		if err then return err end

		-- Register re-runs on every ReloadLua, but so does this whole file, so
		-- `installed` is fresh each time and the targets are the vanilla ones
		-- again. The guard only bars a pathological second apply() in one load.
		if installed then return end

		local summary_orig   = GetSponsorSummary
		local descr_orig     = GetSponsorDescr
		local challenge_orig = LandingSiteObject.GetMissionSponsorEffect

		local summary_new   = wrap_summary(summary_orig)
		local descr_new     = wrap_descr(descr_orig)
		local challenge_new = wrap_challenge(challenge_orig)

		-- Plain assignment through SetGlobal, with the read-back §1.4b requires.
		-- If the second or third install fails we return a reason with the first
		-- already live: harmless by construction, because the entry then reads
		-- inactive and every wrapper's inert() check makes it a pass-through.
		local e = SMRFixPack.SetGlobal("GetSponsorSummary", summary_new)
		if e then return e end
		e = SMRFixPack.SetGlobal("GetSponsorDescr", descr_new)
		if e then return e end

		-- Mod code loads while _G.<Class> is still the classdef (classes.lua:71,
		-- swapped for the built class at :1085), so this is a classdef-time
		-- install and survives flattening. LandingSiteObject declares the method
		-- itself and no shipped class derives from it (whole-tree check).
		LandingSiteObject.GetMissionSponsorEffect = challenge_new
		if LandingSiteObject.GetMissionSponsorEffect ~= challenge_new then
			return "could not install the LandingSiteObject:GetMissionSponsorEffect wrapper"
		end
		installed = true

		-- The probe's surface. Both the wrapper AND the original are exposed so a
		-- probe can tell the two mismatches apart: a live target equal to the
		-- ORIGINAL means our install was lost (a real failure), while one that is
		-- neither means a later mod chained on top of us — the system working,
		-- and it must never read as a failure.
		SMRFixPack.SpaceYDroneCapBullet = {
			stats          = stats,
			summary_new    = summary_new,
			descr_new      = descr_new,
			challenge_new  = challenge_new,
			summary_orig   = summary_orig,
			descr_orig     = descr_orig,
			challenge_orig = challenge_orig,
			bullet_for     = bullet_for,
			ids = { help = HELP_ID, effect = EFFECT_ID },
			prop = PROP,
		}
	end,
})
