-- C89 — ⚖️ A JUDGMENT CALL, NOT A REPAIR OF A CODE ERROR. Four factions count a
-- dome of any size when they judge "more than 10% Unemployment"; the fifth, the
-- Justice Movement, waits until the dome has ten colonists. This module applies
-- the Justice Movement's own rule to the other four, and to the three
-- homelessness twins that carry the same asymmetry. Nothing about the shipped
-- behaviour is a code error, and no surface here may say the game was wrong.
-- Owner ruling: checklist 157 (c), 2026-09-12. Entry: bugs/C89.md.
--
-- THE ASYMMETRY (SOURCE, 1.1.0.403908). ⚠️ The EXPRESSIONS are byte-identical on
-- 1.0.7 but the LIKE IDS ARE NOT, so this module declines there — see the branch
-- guard note below:
--   guarded   JusticeMovement.lua:104  #obj.labels.Colonist >= 10 and #Unemployed*100 >= 10*#Colonist
--             JusticeMovement.lua:129  the same, for Homeless
--   unguarded ProsperityForMars.lua:225    ProsperityUnemployment
--             MarsDemocraticParty.lua:88   UtopiaUnemployment      :107  UtopiaHomeless
--             WorkersParty.lua:114         CollectiveUnemployment  :133  CollectiveHomeless
--             NewSol.lua:47                NewSolUnemployment      :66   NewSolHomeless
-- Without the gate a dome of three with one idle colonist is "more than 10%
-- unemployment", and a filling dome whose workplaces are still under construction
-- trips it every hour until the jobs exist — the early game, which is where this
-- matters and where these factions' positives do not yet exist.
--
-- Patch approach: a DataPatch (FIX_POLICY §1 technique 1) that WRAPS each of the
-- seven likes' DomeFilter.eval, keeping the shipped expression in a closure. The
-- shipped expression is never rewritten and Justice is never touched.
--
-- ⭐ WHY A LIVE FIELD REPLACEMENT WORKS HERE, where C88's message reactions need an
-- additive handler: FactionLikeDomes:CountDome reads `self.DomeFilter and
-- self.DomeFilter.eval` AT CALL TIME (Lua/Factions/FactionDef.lua:857), so
-- replacing the field on the live like object takes effect at the next hourly
-- recalc. Nothing captured the old reference.
--
-- ⛔ THE THRESHOLD IS READ FROM THE GAME, NOT HARD-CODED — and read as BEHAVIOUR,
-- not as a field name (the house rule: check the thing, never its label). Justice's
-- own eval is probed on synthetic domes of 1..200 colonists, every colonist idle
-- and homeless so the percentage clause is always satisfied; the colonist count at
-- which it flips from false to true IS its gate. That probe needs no knowledge of
-- ScriptAND / ScriptCheckLabelCount field names, follows the developers if they
-- rebalance 10 to something else, and declines if Justice ever loses the guard —
-- because then the precedent this module copies is gone.
--
-- ⛔ A LIKE THAT IS ALREADY GATED IS SKIPPED, NOT DOUBLE-GATED, and that test is
-- behavioural too: the like's current eval is called on a dome one colonist below
-- the threshold with every colonist idle and homeless. False ⇒ a gate is already
-- there (the developers added it, or we did on an earlier pass) ⇒ skip. That makes
-- the pass idempotent by construction, which DataPatch requires, and it makes the
-- module stand down per like on the day Paradox ships the same change.
--
-- Calling these evals is safe: each is a generated script-condition body that does
-- arithmetic on two label arrays and returns a boolean — no engine call, no
-- allocation, no yield (the shipped bodies are in the files cited above).
--
-- The gate mirrors Justice byte-for-byte, `#obj.labels.Colonist >= <threshold>`.
-- `labels.Colonist` is always present and non-empty at a real call site: CountDome
-- returns 0 on `not next(dome.labels.Colonist)` BEFORE it reaches the filter
-- (FactionDef.lua:850), and Justice's shipped guard indexes it the same way.
--
-- FIX_POLICY §3a: layer 2 — inert trace, and it is the trace vanilla already has.
--   * Nothing is persisted by us. Preset objects are persist PERMANENTS, keyed
--     "Preset:<class>.<group>.<name>" (CommonLua/Preset.lua:1417-1451), so a
--     FactionDef reached from a save is stored by NAME and restored by lookup; the
--     wrapped eval lives only in the preset, and removing the mod restores the
--     shipped expression at the next load, with the next hourly recalc reading it.
--   * ⚠️ ONE EXPOSURE, MEASURED AND INERT. `FactionsHolder:RecalcFactionsApproval`
--     stores likes_data on g_FactionsHolder, and each row carries
--     `like = <the FactionLikeDomes object>` (FactionDef.lua:67, Factions.lua:685).
--     That NESTED object is not itself a permanent, so a save serialises it by
--     value — its DomeFilter.eval included. This is not new: vanilla's eval is a
--     function value on the same field of the same object, so every existing save
--     already carries that shape. And the field is DEAD — nothing in the shipped
--     tree reads `likes_data[*].like` (only `.id`, `.text`, `.value`, `.how_to`
--     are read: Factions.lua:674-676, :1169, _fixup.lua:2600). The live evaluator
--     reads the PRESET via ForEachPreset, never the snapshot, and the snapshot is
--     overwritten every game hour. So a captured copy is never called, by us or by
--     anyone; the engine's __unpersisted_function__ fallback
--     (CommonLua/Core/persist.lua:52-54) is the backstop, not the mechanism.
--   * A dislike that DISAPPEARS fires no notification: AddFactionLikeDislikeNotification
--     is called only for a like id absent from the previous hour's list
--     (Factions.lua:672-678). So a player installing this update sees dislikes stop
--     arriving, never a burst.
--
-- BRANCH GUARD (FIX_POLICY §2a) — no version check anywhere. The pass declines
-- unless, on the shipped data in front of it: all seven likes exist by Id, each
-- carries a DomeFilter with a function eval, and every like carrying a precedent id
-- gates on the dome's colonist count, all at the same threshold. Nothing at all is
-- patched unless all of that holds, because a partial application would leave the
-- five factions inconsistent — which is the very thing this fixes.
--
-- ⭐ AND THAT IS WHAT DECLINES ON 1.0.7, measured against the archived tree. The
-- expressions there are byte-identical, but the IDS are not: 1.0.7 has THREE likes
-- called `JusticeHomeless` — JusticeMovement.lua:123 (guarded),
-- MarsDemocraticParty.lua:102 and WorkersParty.lua:128 (both unguarded) — which
-- 1.1.0 renamed to UtopiaHomeless and CollectiveHomeless. So on 1.0.7 the precedent
-- check finds an UNGATED like carrying a precedent id and stands the module down,
-- deterministically, before a single eval is wrapped. The desk harness runs that
-- leg six times over because the earlier draft's outcome depended on which
-- duplicate `pairs` reached first.
--
-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-12 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- ⚠️ EACH DEFECT IS AN ABSENCE (FIX_POLICY §2b): the regex states the bare
-- expression that is wrong BECAUSE the gate is missing -- a `return (` with no
-- `Colonist >= ` prefix. So DEFECT-GONE fires per like the day the developers add
-- the gate in that position, and the module independently skips that like by its
-- own behavioural test. If they add the gate somewhere else instead, DEFECT-GONE
-- will not fire and the behavioural skip is what stands the module down; these
-- seven rows are watched for class (b)/(e) as well.
-- SRC: none -- a FactionDef preset patch -- no function body of ours replaces a shipped one
-- DEFECT@Data/FactionDef/ProsperityForMars.lua: return \(#obj\.labels\.Unemployed \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   ProsperityUnemployment counts a dome of any size (no Colonist >= 10 gate)
-- DEFECT@Data/FactionDef/MarsDemocraticParty.lua: return \(#obj\.labels\.Unemployed \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   UtopiaUnemployment counts a dome of any size
-- DEFECT@Data/FactionDef/MarsDemocraticParty.lua: return \(#obj\.labels\.Homeless \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   UtopiaHomeless counts a dome of any size
-- DEFECT@Data/FactionDef/WorkersParty.lua: return \(#obj\.labels\.Unemployed \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   CollectiveUnemployment counts a dome of any size
-- DEFECT@Data/FactionDef/WorkersParty.lua: return \(#obj\.labels\.Homeless \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   CollectiveHomeless counts a dome of any size
-- DEFECT@Data/FactionDef/NewSol.lua: return \(#obj\.labels\.Unemployed \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   NewSolUnemployment counts a dome of any size
-- DEFECT@Data/FactionDef/NewSol.lua: return \(#obj\.labels\.Homeless \* 100 >= 10 \* #obj\.labels\.Colonist\)
--   NewSolHomeless counts a dome of any size

local FIX_ID = "FactionDomeSizeGate"

-- The seven unguarded likes, by their own Id. Keyed on the Id rather than on the
-- faction preset id so a faction rename cannot silently drop one; Justice's two
-- ids are deliberately absent, and that is the whole safety of the list.
local TARGET_IDS = {
	ProsperityUnemployment = true,   -- ProsperityForMars.lua:221-227
	UtopiaUnemployment = true,       -- MarsDemocraticParty.lua:84-90
	UtopiaHomeless = true,           -- MarsDemocraticParty.lua:103-109
	CollectiveUnemployment = true,   -- WorkersParty.lua:110-116
	CollectiveHomeless = true,       -- WorkersParty.lua:129-135
	NewSolUnemployment = true,       -- NewSol.lua:43-49
	NewSolHomeless = true,           -- NewSol.lua:62-68
}
local TARGET_COUNT = 7

-- The precedent, and the ONLY likes read for the threshold. Never patched.
local PRECEDENT_IDS = { "JusticeUnemployment", "JusticeHomeless" }

local PROBE_LIMIT = 200   -- bounds the threshold search; Justice's gate is 10

-- Set by apply() only when the self-check passed; read by the pass. See the note
-- at the top of the pass for why this is a flag and not the registry status.
local self_check_passed = false

-- The shipped eval of each like we wrapped, and the threshold we applied. For the
-- kit probe and for the owner's attended A/B console read; never used by the fix.
local shipped_evals = {}
local applied_threshold = false

-- A synthetic dome of `n` colonists, every one of them idle AND homeless, so the
-- percentage clause of any of these evals is satisfied and only a colonist-count
-- gate can make one return false.
local function probe_dome(n)
	local colonist, unemployed, homeless = {}, {}, {}
	for i = 1, n do
		colonist[i], unemployed[i], homeless[i] = i, i, i
	end
	return { labels = { Colonist = colonist, Unemployed = unemployed, Homeless = homeless } }
end

-- Reads a colonist-count gate out of an eval BY BEHAVIOUR: the count at which it
-- flips false -> true, or nil when it is true from a single colonist (no gate) or
-- never true (not the shape we know). Errors are answers: a body that throws on a
-- synthetic dome is not the shape we know, so it declines.
local function gate_of(eval)
	local ok, first = pcall(function()
		if eval(probe_dome(1)) then return 1 end
		for n = 2, PROBE_LIMIT do
			if eval(probe_dome(n)) then return n end
		end
	end)
	if not ok or type(first) ~= "number" or first < 2 then return nil end
	-- monotone: still true well above the transition, still false just below it
	local ok2, monotone = pcall(function()
		return eval(probe_dome(first + 1)) and not eval(probe_dome(first - 1))
	end)
	if not (ok2 and monotone) then return nil end
	return first
end

-- Is this like's eval already gated at `threshold`? Behavioural, so it sees the
-- developers' own future gate and our own earlier pass alike.
local function already_gated(eval, threshold)
	local ok, res = pcall(eval, probe_dome(threshold - 1))
	return ok and not res
end

-- Walk every FactionDef's likes once. `visit(like, faction)` per like.
local function for_each_like(visit)
	local defs = rawget(_G, "FactionDefs")
	if type(defs) ~= "table" then return false end
	local seen = 0
	for _, faction in pairs(defs) do
		if type(faction) == "table" and type(faction.likes) == "table" then
			for _, like in ipairs(faction.likes) do
				if type(like) == "table" then
					seen = seen + 1
					visit(like, faction)
				end
			end
		end
	end
	return seen > 0
end

local function eval_of(like)
	local filter = like.DomeFilter
	if type(filter) ~= "table" then return nil end
	local eval = filter.eval
	if type(eval) ~= "function" then return nil end
	return eval, filter
end

local patch = SMRFixPack.DataPatch(FIX_ID, {
	changed_class = "FactionDef",
	pass = function(ctx)
		-- ⛔ THE PASS MUST CONFIRM THE SELF-CHECK PASSED (FIX_POLICY §2, the A1 lesson
		-- applied to a DataPatch). DataPatch's runner re-reads the veto before every
		-- pass but NOT the apply verdict (00_Core.lua's `run`), and its OnMsg handlers
		-- are installed at file scope — so a module whose apply() DECLINED would still
		-- have its pass patch shipped data on ClassesBuilt while the entry and the log
		-- both read `inactive`. Filed as a shared defect (bugs/C90.md — it reaches
		-- Fix_SaintBlessing and Fix_SinkholeIndestructible too); this module does not
		-- wait for that repair.
		-- ⚠️ The flag, not `SMRFixPack.fixes[id].status`: run_apply writes the status
		-- only AFTER apply returns, so on a live re-apply the pass legitimately runs
		-- while the status still holds its previous value. The flag is exact and
		-- order-independent.
		if not self_check_passed then return end

		if not rawget(_G, "FactionDefs") then
			-- ⛔ Absence proves nothing until DataLoaded has fired (the F75 lesson);
			-- the runner tracks that for us.
			if ctx.data_loaded then
				ctx.latch("the FactionDefs preset map is gone")
			end
			return
		end

		-- 1 · The precedent. Read Justice's threshold from its own behaviour, and
		--     require both of its likes to agree — one of them disagreeing means
		--     the shape is not what this module copies.
		-- ⚠️ EVERY like carrying a precedent id must be gated, and they must agree —
		-- not just the first one found. On the 1.0.7 tree THREE factions share the id
		-- `JusticeHomeless` (JusticeMovement.lua:123 guarded, MarsDemocraticParty.lua:102
		-- and WorkersParty.lua:128 unguarded); 1.1.0 renamed the latter two to
		-- UtopiaHomeless / CollectiveHomeless. Reading only one of them would make the
		-- outcome depend on `pairs` order over FactionDefs. Requiring all of them makes
		-- the module decline on 1.0.7 deterministically, with a reason — which is
		-- exactly what a branch guard is for (FIX_POLICY §2a), and it needs no version
		-- check to do it.
		local precedent_is = {}
		for _, id in ipairs(PRECEDENT_IDS) do precedent_is[id] = true end
		local threshold, bad_precedent, seen_precedent = nil, nil, 0
		for_each_like(function(like, faction)
			local id = like.Id
			if id and precedent_is[id] then
				seen_precedent = seen_precedent + 1
				local eval = eval_of(like)
				local t = eval and gate_of(eval) or nil
				if not t then
					bad_precedent = bad_precedent or string.format(
						"%s on %s carries no dome-size gate", tostring(id),
						tostring(faction and faction.id))
				elseif threshold and threshold ~= t then
					bad_precedent = bad_precedent or string.format(
						"the shipped dome-size gates disagree (%d vs %d)", threshold, t)
				else
					threshold = t
				end
			end
		end)
		if bad_precedent or not threshold or seen_precedent < #PRECEDENT_IDS then
			if ctx.data_loaded then
				ctx.latch(bad_precedent
					or (not threshold and "no shipped dislike gates on the dome's colonist count")
					or string.format("%d of %d precedent dislikes found",
						seen_precedent, #PRECEDENT_IDS),
					"the precedent this judgment call copies is not present as expected: "
					.. tostring(bad_precedent or "gate not found"))
			end
			return
		end

		-- 2 · The seven targets. Every one must be present and shaped as expected,
		--     or nothing is patched at all — a partial application would leave the
		--     five factions inconsistent, which is the thing this fixes.
		local targets, broken = {}, nil
		for_each_like(function(like, faction)
			local id = like.Id
			if id and TARGET_IDS[id] then
				local eval, filter = eval_of(like)
				if not eval then
					broken = broken or (tostring(id) .. " has no DomeFilter.eval function")
				else
					targets[#targets + 1] = { id = id, like = like, filter = filter,
						eval = eval, faction = faction.id }
				end
			end
		end)
		if broken then
			if ctx.data_loaded then ctx.latch(broken) end
			return
		end
		if #targets ~= TARGET_COUNT then
			if ctx.data_loaded then
				ctx.latch(string.format("%d of %d gated faction dislikes found",
					#targets, TARGET_COUNT))
			end
			return
		end

		-- 3 · Apply. A like already gated — by the developers, or by our own earlier
		--     pass — is skipped, never double-gated.
		local changed, skipped = 0, {}
		for _, t in ipairs(targets) do
			if already_gated(t.eval, threshold) then
				skipped[#skipped + 1] = t.id
			else
				local orig = t.eval
				t.filter.eval = function(obj)
					return #obj.labels.Colonist >= threshold and orig(obj)
				end
				-- Kept for the owner's attended A/B: it lets one console line ask
				-- "what would the shipped rule have said about THIS dome?" beside what
				-- the live rule says, which is the leg's falsifier. Read-only, and it
				-- is the same function value the preset already held.
				shipped_evals[t.id] = orig
				changed = changed + 1
			end
		end
		applied_threshold = threshold

		ctx.patched = true
		if changed > 0 then
			ctx.ever_changed = true
			SMRFixPack.Log("%s: %d faction dislike(s) now wait for %d colonists in a dome%s",
				FIX_ID, changed, threshold,
				#skipped > 0 and (" (" .. #skipped .. " already gated: "
					.. table.concat(skipped, ", ") .. ")") or "")
		elseif not ctx.ever_changed then
			-- B3: nothing to change AND we never changed anything in this process
			-- ⇒ the shipped data already carries the gate everywhere. That is the
			-- developers having made the same call, which is the RETIRE signal.
			ctx.latch("every faction dislike already waits for " .. tostring(threshold)
				.. " colonists in a dome", nil, "benign")
		end
	end,
})

-- Exposed for the TestKit's behaviour probe: the live evals, the threshold that
-- was applied, and which likes were skipped. A table of functions on the mod's own
-- global — precedent SMRFixPack.Sanitizer (90_SaveSanitizer.lua:402). Nothing
-- persisted reaches SMRFixPack, so this stores no function value the save can see.
SMRFixPack.FactionDomeGate = {
	TargetIds = TARGET_IDS,
	PrecedentIds = PRECEDENT_IDS,
	ProbeDome = probe_dome,
	GateOf = gate_of,
	ForEachLike = for_each_like,
	EvalOf = eval_of,
	Shipped = shipped_evals,
	Threshold = function() return applied_threshold end,

	-- ⭐ THE OWNER'S ATTENDED A/B, in one call (checklist 158). Give it a dome — the
	-- selected one by default — and it prints, per patched like, what the SHIPPED
	-- rule would have said about that dome beside what the LIVE rule says. Prefixed
	-- so it can be read back from a flushed log, and read-only: it calls only these
	-- evals, which do arithmetic on two label arrays.
	-- ⛔ The control is built in: when the fix is absent or not applied, `shipped`
	-- and `live` are identical on every row, and the line says GATE-ABSENT.
	Report = function(dome)
		dome = dome or rawget(_G, "SelectedObj")
		local labels = type(dome) == "table" and dome.labels
		if type(labels) ~= "table" or type(labels.Colonist) ~= "table" then
			SMRFixPack.Log("C89-AB: select a DOME first (no labels.Colonist on %s)",
				tostring(dome and dome.class))
			return
		end
		SMRFixPack.Log("C89-AB dome=%s colonists=%d unemployed=%d homeless=%d threshold=%s",
			tostring(dome.class), #labels.Colonist,
			#(labels.Unemployed or ""), #(labels.Homeless or ""),
			tostring(applied_threshold))
		local rows, differ = 0, 0
		for id in pairs(TARGET_IDS) do
			local live
			for_each_like(function(like)
				if like.Id == id then live = eval_of(like) end
			end)
			local orig = shipped_evals[id]
			if live then
				rows = rows + 1
				local ok_l, r_live = pcall(live, dome)
				local r_ship, ok_s = nil, true
				if orig then ok_s, r_ship = pcall(orig, dome) else r_ship = "not-wrapped" end
				if ok_l and ok_s and orig and r_live ~= r_ship then differ = differ + 1 end
				SMRFixPack.Log("C89-AB   %-24s shipped=%s live=%s", id,
					tostring(r_ship), tostring(ok_l and r_live))
			end
		end
		SMRFixPack.Log("C89-AB %d row(s), %d where the gate changed the answer -- %s",
			rows, differ,
			differ > 0 and "GATE ACTIVE on this dome"
			or (rows == 0 and "GATE-ABSENT: no target like found"
				or "no difference on this dome (expected when it has "
					.. tostring(applied_threshold) .. "+ colonists, or the fix is off)"))
	end,
}

SMRFixPack.Register(FIX_ID, {
	title = "Judgment call: all five factions wait for ten colonists in a dome "
		.. "before disliking its unemployment or homelessness",
	apply = function()
		local err = SMRFixPack.Require(FIX_ID, {
			{ class = "FactionLikeDomes", method = "CountDome" },
		})
		if err then return err end
		self_check_passed = true
		patch()   -- no-op at apply time (F87); the runner fires itself once the
		          -- classes are built AND the presets are loaded
	end,
})
