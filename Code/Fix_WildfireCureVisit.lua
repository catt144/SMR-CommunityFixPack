-- C108: the Wildfire cure never reaches colonists whose Health is paid at home,
-- so the mystery cannot finish once they are served from home.
--
-- Defect (1.1.0.403908): the cure clears `Infected` in one place, a medical
-- visit: MedicalBuilding:Service, once g_StartVaccinating is set
-- (Lua/Buildings/MedicalCenter.lua:35-46; the flag is set by
-- OnMsg.Mystery8_BeginHealing, Lua/Traits.lua:1227-1229). The mystery promises
-- "cured permanently after their first visit in a Medical Building"
-- (Data/Scenario/Mystery 8.lua:204) and ends only when no colonist is infected
-- (:1045-1051). A colonist goes to a medical building for itself only when
-- Health < HighStatLevel (70) or Sanity is low (Lua/Units/Colonist.lua:2313-2333).
-- 1.1.0 pays every service category's stats at home, on every rest
-- (ApplyResidenceAdditiveStats, Lua/Stats.lua:623-648, called at Colonist.lua:2605),
-- and the medical buildings are a category like any other: Infirmary and Medical
-- Post pay +10 Health, Medical Center and Hospital +20 (Data/BuildingTemplate/*,
-- all `same_category_as = "Infirmary"`). Infected costs 12 Health a sol
-- (Data/TraitPreset.lua:144-157), and 1.1.0 dropped the old +5 rest recovery
-- (DailyHealthRecover = 0, Colonist.lua:164). So a colonist under a Medical
-- Center nets +8 a sol, never drops below 70, never visits and is never cured.
-- On 1.0.7 the same colonist netted -7 (rest +5, Colonist.lua:2026 there) and
-- reached the visit threshold within five sols. Full evidence: docs/agent/bugs/C108.md.
--
-- Intent tell 4 (self-contradiction): the mystery's own text names the visit as
-- the cure and waits for zero infected. Once medical coverage is paid at home,
-- the more medical care a dome has, the less its infected are ever sent to it.
--
-- Repair: once vaccination has started, an infected colonist's interest for the
-- sol is "needMedical". Colonist:Idle visits the daily interest
-- (Colonist.lua:2383-2386), Dome:GetService finds a medical building by that
-- interest (every medical template has interest1 = "needMedical"), and the visit
-- ends in MedicalBuilding:Service (Colonist.lua:2482), which cures. The game
-- already uses this route to send a colonist to a medical building while healthy:
-- the Hypochondriac trait adds the same interest (Data/TraitPreset.lua:116-126).
-- The daily interest in 1.1.0 is a cosmetic visit (its own comment,
-- Colonist.lua:2382), so an infected colonist gives up nothing but one sol's
-- sightseeing, once: the cure removes the trait and the next sol picks as usual.
-- Not done instead: curing on the at-home medical payment. That would cure
-- without the visit the text names, and would still miss a colonist whose Health
-- is held up by something else (an Open Air Gym, a Tai Chi Garden, a Smart Home,
-- Feeding the Future delicacies).
--
-- Patch approach: FIX_POLICY §1.4b chained POST-wrapper on the global
-- PickInterest. The shipped body always runs, so the colonist's random stream
-- draws exactly what vanilla draws; only its answer is replaced, and only for
-- an infected colonist while g_StartVaccinating is set. Every other call returns
-- vanilla's value untouched. Callers: Colonist:Init and Colonist:DailyUpdate
-- (Colonist.lua:294, :722), both assigning daily_interest; nothing else calls it.
-- Layer: §3a layer 3 — a synchronous function with no yield; nothing of ours is
-- on a stack that can be saved, and nothing is stored in the save. A save made
-- with the pack loads without it; an infected colonist then simply goes back to
-- the shipped behaviour.
--
-- Branch guard (§2a): a behaviour probe of the SHIPPED AccumulateCategoryServiceStats
-- on stub tables: it must add a category's Health to the colonist's total. That
-- is the at-home payment that hides the need to visit. It does not exist on
-- 1.0.7 (zero hits for the name there), so the module declines on that branch,
-- where colonists still reach the threshold and the defect does not occur.

-- MANIFEST (FIX_POLICY §2b) -- machine-read by `python tools/bodycheck.py`.
-- Pinned 2026-09-18 against shipped game 1.1.0.403908. ⛔ These are CLAIMS about
-- the shipped tree, not a clearance: re-pin them deliberately when a target moves,
-- never to silence a BODY-CHANGED.
-- SRC: Lua/Buildings/MedicalCenter.lua MedicalBuilding:Service sha256=f4c1e89466190960a815f163b6702fe2ef40d7029ae3cfa542f0334797ebe28e
--   (Lua/Buildings/MedicalCenter.lua:35-46 at pin time)
-- DEFECT: if\s+unit\.traits\.Infected\s+and\s+g_StartVaccinating\s+then
--   the cure lives only in a visit; a patch that moves it (to the at-home
--   payment, say) stops the match. An absence defect (§2b): a visit trigger
--   added elsewhere for infected colonists will not fire DEFECT-GONE
-- SRC: Lua/Stats.lua ApplyResidenceAdditiveStats sha256=6382f0c722a1a81c5c1f2f72dd51c1e7ff74efaf62807c4708cc8c1136ad7c8f
--   (Lua/Stats.lua:623-648 at pin time)
-- DEFECT: AccumulateCategoryServiceStats\(totals,\s*category_data,\s*ColonistAdditiveStatList,\s*colonist\)
--   every serviced category, the medical one included, paid at home on rest
-- SRC: Lua/Interests.lua PickInterest sha256=d9c27ae09546365a180cd8b550c6e6a6babd66b9dffba37d805e903076c76219
--   (Lua/Interests.lua:112-114 at pin time). No defect line on purpose: this is
--   the function we wrap, pinned for class (b) only; there is no fault in it

local FIX_ID = "WildfireCureVisit"
local MEDICAL = "needMedical"

-- STUB CONTRACT (FIX_POLICY §2a), read from the shipped 1.1.0
-- AccumulateCategoryServiceStats (Lua/Stats.lua:568-582):
--   * category_data  filter_name "Everyone", so the filter branch (:570-578) is
--                    skipped before it reads ColonistFilterFunc or the colonist;
--   * stat_list      given, so the ColonistTargetStatList default (:579) is not read;
--   * out            a plain table the body adds into (:581).
-- Synchronous, no Msg, no global write: the one write lands on the stub `out`.
-- The verdict: `out.Health` went from 0 to the category's 7000. The 1.0.7 tree
-- has no such global, so the `test` before it declines first there.
local function pays_category_health_at_home()
	local out = { Health = 0 }
	AccumulateCategoryServiceStats(out, { filter_name = "Everyone", Health = 7000 },
		{ "Health" }, { traits = {} })
	return out.Health == 7000
end

SMRFixPack.Register(FIX_ID, {
	title = "Once the Wildfire cure is found, infected colonists visit a medical building and are cured, so the mystery can finish",
	apply = function()
		-- MedicalBuilding declares Service itself (MedicalCenter.lua:35), so the
		-- pre-flattening check sees it (the F64 lesson). Nothing is captured from
		-- it: it is checked because the repair is pointless without the cure there.
		local err = SMRFixPack.Require(FIX_ID, {
			{ global = "PickInterest" },
			{ class = "MedicalBuilding", method = "Service" },
			-- A `test`, not `{ global = }`: on 1.0.7 the name is absent by design,
			-- and that decline is correct, not patch rot (no update_suspect).
			{ test = function() return type(rawget(_G, "AccumulateCategoryServiceStats")) == "function" end,
			  reason = "no at-home service payment (AccumulateCategoryServiceStats): the colonists this fix is for still reach a medical building on their own on this game version" },
			{ probe = pays_category_health_at_home,
			  reason = "the at-home service payment does not pay a category's Health the way this fix expects (behaviour probe declined)" },
		})
		if err then return err end
		local orig = PickInterest

		return SMRFixPack.SetGlobal("PickInterest", function(unit, ...)
			-- vanilla always runs first: its random draw is the colonist's to make
			local interest = orig(unit, ...)
			if not rawget(_G, "g_StartVaccinating") or type(unit) ~= "table" then
				return interest
			end
			local traits = unit.traits
			if type(traits) ~= "table" or not traits.Infected then
				return interest
			end
			if not SMRFixPack.IsActive(FIX_ID) then return interest end
			-- FIX (C108): the cure is given on a medical visit, and a colonist whose
			-- Health is paid at home is never sent on one. Send them.
			return MEDICAL
		end, "could not install the PickInterest wrapper")
	end,
})
