-- C51: three player-visible strings can never be translated, while their
-- translations sit in every shipped language pack.
--
-- ⭐ NOTHING HERE IS RE-WORDED. This module changes no text. It points two
-- controls at translation ids that already ship, and that is the whole fix.
--
-- ── The defect, two misses ────────────────────────────────────────────────
-- (1) The terraforming overview's panel title is a RAW LUA STRING with no
--     translation id at all: `Text = "OVERALL TERRAFORMING PROGRESS"`,
--     Lua\XDef\TerraformingOverall.generated.lua:56 (mirrored in the editor
--     source, Data\XDef\TerraformingOverall.lua:51). A plain string carries no
--     id, so the localization system never sees it — while the identical
--     English text IS an enrolled record, `T(914616772802, "OVERALL
--     TERRAFORMING PROGRESS")`, Lua\LocalizationTexts.lua:246.
-- (2) The Universal Rocket's *Back to Earth* infopanel button uses two ids that
--     NO language pack contains — `T(807999655245, …)` and `T(885571832096, …)`,
--     Lua\XDef\customUniversalRocket.generated.lua:23-24 — while the identical
--     English text ships under `T(316233855405, …)` and `T(407456913268, …)`,
--     Lua\LocalizationTexts.lua:357-358.
--
-- ── The measurement (RE-DERIVED 2026-08-20 for this build, not inherited) ──
-- All nine shipped packs under `Local\` were extracted with this repo's own
-- tools\flpk_extract.py and their `CurrentLanguage/Game.csv` read directly
-- (Brazilian, English, French, German, Polish, Russian, Schinese, Spanish,
-- Turkish — 23,090 CSV records each). Every one of the three REPLACEMENT ids is
-- present in all nine; both ids the rocket button uses are ABSENT from all nine.
-- German: 914616772802 → "TERRAFORMING-GESAMTFORTSCHRITT", 407456913268 →
-- "Zurück zur Erde", 316233855405 → the full German sentence.
--
-- ⭐ AND THE ENGLISH CASE IS SAFE BY THE LOADER'S OWN RULE, which is the part
-- worth re-reading before touching this file. In `English.fpk` those three rows
-- carry an EMPTY `Translation` column (22,266 of 23,090 rows do). That is not a
-- gap: `csv_load_fields` maps column 2 → `text` and column 3 → `translated_new`
-- (CommonLua\Core\localization.lua:920), and `ProcessLoadedTables` (:938-960)
-- resolves English in the order { translated_new, TEXT, translated } — so
-- `TranslationTable[914616772802]` is the English source string itself. Every
-- row in a pack lands in the table; an English player sees exactly the words
-- they see today, and the other eight see their own.
--
-- ── Why this cannot regress anything (EF-039, read forwards for once) ──────
-- `T(id, text)` ends with `if not dev and not Platform.ged and
-- TranslationTable[id] then return LocIdToLightUserdata(id) end`
-- (localization.lua:250-252, sibling branch :270-272), and rendering then reads
-- `TranslationTable[id]` (:662). In retail, therefore, a `T()` on an ENROLLED
-- id discards our literal and prints the shipped translation — no English
-- literal is anywhere in the path. That is the mechanism that made
-- Fix_TechDescriptionBuilding a shipped no-op (F98); here it is the mechanism
-- working FOR us. The English literals passed below are byte-identical to the
-- shipped ones, so a dev/Ged build (where the light-userdata branch is skipped)
-- also renders the correct words.
--
-- ── Technique: chain, never replace (FIX_POLICY §1.4) ─────────────────────
-- Both targets are XDef-generated `Init` methods declared on their own class
-- (verified at ModTools\Src, pinned build 1.0.7.396349, EF-014 — ⚠️ `Src` is
-- under the install dir literally named `Project Spark`; the old
-- `Surviving Mars` folder's ModTools has no `Src` and is a decoy):
--   TerraformingOverall:Init      — TerraformingOverall.generated.lua:18
--   customUniversalRocket:Init    — customUniversalRocket.generated.lua:11
-- We capture whatever `Init` is installed when we load — if another mod
-- replaced it first, THAT version is our original and their work stays in the
-- chain — call it first, and correct the controls it built. Mod code loads
-- before class flattening (`_G.<Class>` is still the classdef, classes.lua:71,
-- swapped for the built class at :1085), so this is a classdef-time install and
-- it propagates through flattening — which matters, because
-- `customUniversalRocket` has FIVE subclasses that declare no `Init` of their
-- own (Dragon/Lander/Refugee/Trade/Zeus, Data\XDef\customUniversal*Rocket.lua).
-- They all inherit the repair.
--
-- ── Handles (FIX_POLICY §2) ───────────────────────────────────────────────
-- The rocket button carries `Id = "idBackToEarth"` (:25) and is a DIRECT child
-- of the window Init built, so it is found by id — never by text. ⛔ The
-- terraforming heading has NO id: its only possible handle is the English
-- literal it renders, so that is what we match, and we match it exactly and
-- only on a plain Lua string. The consequence is deliberate and is the safe
-- direction: the day a patch re-words it, gives it an id, or fixes it outright,
-- the match fails, this module stands down with a reason line in our log, and
-- the player sees vanilla. It never guesses at a control.
--
-- Both sites also verify the REMEDY before applying it — the replacement id
-- must actually be in the loaded `TranslationTable` — and the rocket site
-- verifies the DEFECT by reading the id currently on the control (`TGetID`,
-- localization.lua:48-61) rather than assuming it. Nothing is overwritten
-- blind, and a language change mid-session re-runs those checks, because they
-- live at panel-build time and not at apply time.
--
-- ── §3a layer statement: LAYER 3 — nothing of ours enters a save ──────────
-- ⭐ THIS MODULE WRITES NOTHING. No persisted class, no GameVar, no game-time
-- thread, no `OnMsg.LoadGame`, no state of any kind: it is UI text and it is
-- rebuilt from scratch every time a panel opens. Neither route into a savegame
-- is open to it — the wrapper bodies contain no `Sleep`/`WaitMsg`, so no frame
-- of ours can sit below a blocking call; and the only things holding our
-- functions are a class table and an X window, both of which the engine
-- excludes (`XWindow.__persist = false`, XWindow.lua:4). That is what makes
-- this fix free to add to any existing save and free to remove from one.
-- The orphan gate below is a backstop, not the mechanism.
--
-- ── Prior art (FIX_POLICY §8) ─────────────────────────────────────────────
-- fredware's SMR Community Fixes #13, *Restore Localized UI Text*, identified
-- both locations and both replacement ids first. The nine-pack measurement, the
-- English-loader derivation above, and the per-call verification are ours.
--
-- ⛔ UNOBSERVED. No leg of this project has ever watched a shipped-id string
-- render in a non-English language (EF-039's closing note). This module was
-- built and parsed; it has not been seen on a screen.

local ID = "LocalizedUIText"
local log = SMRFixPack.Log

-- Miss 1 — the heading.
local TERRA_LITERAL = "OVERALL TERRAFORMING PROGRESS"
local TERRA_ID      = 914616772802

-- Miss 2 — the button. BROKEN = the id the XDef uses and no pack contains;
-- GOOD = the enrolled id carrying the identical English text.
local ROCKET_BUTTON  = "idBackToEarth"
local TITLE_BROKEN, TITLE_GOOD = 885571832096, 407456913268
local TEXT_BROKEN,  TEXT_GOOD  = 807999655245, 316233855405
local TITLE_EN = "Back to Earth"
local TEXT_EN  = "Send the rocket directly to Earth without any resources."

-- How deep to search for the heading. Its real depth is 3 (dialog → VList →
-- XWindow → XText); the bound only stops a pathological tree from costing us.
local MAX_DEPTH = 6

-- Counters, exposed for the TestKit probe. `reason` holds the FIRST decline at
-- each site — these panels are rebuilt every time the player opens them, so a
-- per-call log line would flood the file.
local stats = {
	heading = { patched = 0, declined = 0, reason = "" },
	rocket  = { patched = 0, declined = 0, reason = "", strings = 0 },
}

local function note_decline(site, reason)
	local s = stats[site]
	s.declined = s.declined + 1
	if s.reason == "" then
		s.reason = reason
		log("%s: %s", ID, reason)
	end
end

-- Is this id reachable by the localization system in the language loaded RIGHT
-- NOW? Re-read per call: the player can change language mid-session and the
-- engine rebuilds the table (options.lua:885).
local function enrolled(id)
	local tt = rawget(_G, "TranslationTable")
	return type(tt) == "table" and tt[id] ~= nil
end

-- Hand the call straight back unless this repair is ours to make (FIX_POLICY
-- §2 — the registry status AND the veto, re-read per call so a mid-session
-- veto works). The SMRFixPack read is the §3a orphan gate: reading a nil global
-- is safe, so a captured copy of this closure would exit here rather than
-- part-way through.
local function inert()
	local pack = rawget(_G, "SMRFixPack")
	if type(pack) ~= "table" or not pack.IsActive(ID) then return true end
	local vetoed = rawget(_G, "SMRFixPack_Disabled")
	if type(vetoed) == "table" and vetoed[ID] then return true end
	return false
end

---- miss 1 — the heading with no id --------------------------------------

-- Depth-bounded search for the XText still carrying the raw English literal.
-- Matching requires a PLAIN STRING: once the control holds a T value (ours, a
-- patch's, or another mod's) it is not a match and we leave it alone.
local function find_literal(win, depth)
	for _, child in ipairs(win) do
		if type(child) == "table" then
			local text = child.Text
			if type(text) == "string" and text == TERRA_LITERAL then
				return child
			end
			if depth < MAX_DEPTH then
				local found = find_literal(child, depth + 1)
				if found then return found end
			end
		end
	end
end

local function patch_heading(win)
	local ctrl = find_literal(win, 1)
	if not ctrl then
		return note_decline("heading",
			"the OVERALL TERRAFORMING PROGRESS heading was not found by its literal text — nothing changed (a game update reworked TerraformingOverall, another mod got there first, or it already carries a translation id)")
	end
	if type(ctrl.SetText) ~= "function" then
		return note_decline("heading", "the heading control has no SetText — nothing changed")
	end
	if not enrolled(TERRA_ID) then
		return note_decline("heading",
			string.format("translation id %d is not in this build's language table — nothing changed", TERRA_ID))
	end
	-- Translate first: XTranslateText:SetText asserts on the combination
	-- (Translate == false, value is a T) even though it would translate anyway
	-- via IsT (XControl.lua:541-555). The generated setter for a property with
	-- no `invalidate` is a plain assignment (_X.lua:78-81), so this IS the
	-- setter.
	ctrl.Translate = true
	ctrl:SetText(T(TERRA_ID, TERRA_LITERAL))
	stats.heading.patched = stats.heading.patched + 1
	if stats.heading.patched == 1 then
		log("%s: terraforming heading now renders translation id %d", ID, TERRA_ID)
	end
end

---- miss 2 — the button using ids no pack knows ---------------------------

local function patch_rocket(win)
	local btn
	for _, child in ipairs(win) do
		if type(child) == "table" and child.Id == ROCKET_BUTTON then
			btn = child
			break
		end
	end
	if not btn then
		return note_decline("rocket",
			"the Back to Earth button (Id " .. ROCKET_BUTTON .. ") was not built by this panel — nothing changed (a game update renamed or removed it, or another mod rebuilt the panel)")
	end
	if type(btn.SetRolloverTitle) ~= "function" or type(btn.SetRolloverText) ~= "function" then
		return note_decline("rocket", "the Back to Earth button has no rollover setters — nothing changed")
	end
	local id_of = rawget(_G, "TGetID")
	if type(id_of) ~= "function" then
		return note_decline("rocket", "TGetID is not available — the ids on the button cannot be read, so nothing changed")
	end

	-- Repoint only what still carries the unenrolled id AND only where the
	-- replacement resolves. If a patch ever enrols the shipped ids, or rewires
	-- the XDef, both tests fail and we do nothing.
	local done = 0
	if id_of(btn.RolloverTitle) == TITLE_BROKEN and enrolled(TITLE_GOOD) then
		btn:SetRolloverTitle(T(TITLE_GOOD, TITLE_EN))
		done = done + 1
	end
	if id_of(btn.RolloverText) == TEXT_BROKEN and enrolled(TEXT_GOOD) then
		btn:SetRolloverText(T(TEXT_GOOD, TEXT_EN))
		done = done + 1
	end
	if done == 0 then
		return note_decline("rocket",
			"the Back to Earth button no longer carries the two unenrolled ids, or their replacements are not in this build's language table — nothing changed")
	end
	stats.rocket.patched = stats.rocket.patched + 1
	stats.rocket.strings = stats.rocket.strings + done
	if stats.rocket.patched == 1 then
		log("%s: Back to Earth rollover now renders translation ids %d / %d (%d of 2 strings)",
			ID, TITLE_GOOD, TEXT_GOOD, done)
	end
end

---- the chain -------------------------------------------------------------

-- Call the original first and pass its returns through (FIX_POLICY §1.4), then
-- correct what it built. The pass runs under pcall because it executes inside
-- engine UI construction: a throw here would take the whole panel down, and a
-- cosmetic repair must never be able to do that.
local function chain(orig, patch, site)
	return function(self, ...)
		local r1, r2, r3 = orig(self, ...)
		if not inert() then
			local ok, err = pcall(patch, self)
			if not ok then
				note_decline(site, "the " .. site .. " pass raised and was contained: " .. tostring(err))
			end
		end
		return r1, r2, r3
	end
end

local installed = false

SMRFixPack.Register(ID, {
	title = "Three UI strings render in English in every language — the terraforming heading and the rocket's Back to Earth rollover now use the translation ids the game already ships",
	apply = function()
		local err = SMRFixPack.Require(ID, {
			{ global = "T" },
			{ global = "TGetID" },
			{ global = "TranslationTable", kind = "table" },
			{ class = "TerraformingOverall", method = "Init" },
			{ class = "customUniversalRocket", method = "Init" },
			-- Content checks, not shape checks: these say the defect is still
			-- the defect and the remedy still exists. Require does not mark
			-- `test` failures as patch rot, which is right — an upstream fix is
			-- not a game-update suspect.
			{ test = function() return enrolled(TERRA_ID) and enrolled(TITLE_GOOD) and enrolled(TEXT_GOOD) end,
				reason = "this build's language pack does not carry all three replacement records — there is nothing to point the UI at" },
			{ test = function() return not enrolled(TITLE_BROKEN) and not enrolled(TEXT_BROKEN) end,
				reason = "the ids the Back to Earth button uses now resolve in this build's language pack — the game fixed this upstream" },
		})
		if err then return err end

		-- Register re-runs on every ReloadLua, but so does this whole file, so
		-- `installed` is fresh each time and the classdefs are rebuilt with it.
		-- The guard only bars a pathological second apply() inside one load.
		if installed then return end

		local terra_orig  = TerraformingOverall.Init
		local rocket_orig = customUniversalRocket.Init
		local terra_init  = chain(terra_orig, patch_heading, "heading")
		local rocket_init = chain(rocket_orig, patch_rocket, "rocket")

		TerraformingOverall.Init  = terra_init
		customUniversalRocket.Init = rocket_init

		-- Read back, the way §1.4b requires of a replacement: if either write
		-- did not land, say so instead of reporting active over nothing.
		if TerraformingOverall.Init ~= terra_init then
			return "could not install the TerraformingOverall.Init wrapper"
		end
		if customUniversalRocket.Init ~= rocket_init then
			return "could not install the customUniversalRocket.Init wrapper"
		end
		installed = true

		-- The probe's surface. Both the wrapper AND the original are exposed so
		-- a probe can tell the two mismatches apart: a live Init equal to the
		-- ORIGINAL means our install was lost (a real failure), while an Init
		-- that is neither means a later mod chained on top of us, which is the
		-- system working and must never read as a failure.
		SMRFixPack.LocalizedUIText = {
			stats       = stats,
			terra_init  = terra_init,
			rocket_init = rocket_init,
			terra_orig  = terra_orig,
			rocket_orig = rocket_orig,
			ids = {
				heading      = TERRA_ID,
				title_broken = TITLE_BROKEN, title_good = TITLE_GOOD,
				text_broken  = TEXT_BROKEN,  text_good  = TEXT_GOOD,
			},
		}
	end,
})
