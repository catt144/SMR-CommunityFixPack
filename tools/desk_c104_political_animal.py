#!/usr/bin/env python3
"""C104 investigation: can Political Animal ("Enact all laws") be earned on 1.1.0?

Executes the SHIPPED registries (every PolicyCategoryDef / PolicyDef / LawDef preset
file, base game and Norman DLC) and the SHIPPED decision bodies: ForEachPreset,
ScriptProgram:__call, GetAllExplanations, LawDef/PolicyDef:EvalDisableConditions,
LawDef:Activate/Deactivate, GetPolicyLaws, UpdatePolicyLawCache, GetPolicyDefaultLaw,
Legislature:RecalcPoliciesState/IsPolicyPrepared/IsActionOnCd,
CheckPoliticalAnimalAchievement, RevokeLawsDueToConditions, and the state readers the
disable conditions and prerequisites call.

Retyped or stubbed, and why each is safe for THIS question:
  * PlaceObj / T / set / Untranslated -- registry construction; decide nothing.
  * law effects (CreateInstance/ApplyEffects/UnapplyEffects) -- no LawDef in either
    shipped tree repeals ANOTHER law from its effects (grep of Data/LawDef +
    DLC/norman/Presets/LawDef for Deactivate/Activate: the one hit is FounderPrivilege
    removing itself when the last Founder dies, and FounderPrivilege is exempt).
  * Msg("LawActivated") -> CheckPoliticalAnimalAchievement(): retypes the Achievement
    MsgReaction at Data/Achievement.lua:849-853.
  * AchievementUnlock -- a counting sink; never contacts Steam.
  * gate_open(): the lock the voting card applies (Data/XDef/LawVotingCard.lua:367-368,
    policy:EvalDisableConditions() or law:EvalDisableConditions()); both calls are the
    shipped bodies.
  * procall is pcall that RECORDS every error, and every leg demands zero -- a missing
    shim would otherwise read as a hidden policy (ScriptProgram:__call returns nothing
    on a throw).

What this is NOT: nothing ran in a game; no player save is modelled; the colony state
is an explicit synthetic fixture chosen so that every NON-law disable condition is
already satisfied, which isolates the law-on-law locks.
"""
import glob
import hashlib
import os
import subprocess
import sys

import deskbench as db

REGISTRIES = (
    "Data/PolicyCategoryDef.lua",
    "Data/PolicyDef.lua",
    "DLC/norman/Presets/PolicyDef.lua",
)

BODIES = (
    ("CommonLua/Preset.lua", r"^function ForEachPreset\("),
    ("CommonLua/Scripting.lua", r"^function ScriptProgram:__call\("),
    ("CommonLua/Classes/Explanation.lua", r"^function GetAllExplanations\("),
    ("CommonLua/Features/GameRules.lua", r"^function IsGameRuleActive\("),
    ("CommonLua/LabelContainer.lua", r"^function LabelGetFirst\("),
    ("Lua/Factions/LawDef.lua", r"^function LawDef:IsActive\("),
    ("Lua/Factions/LawDef.lua", r"^function LawDef:Activate\("),
    ("Lua/Factions/LawDef.lua", r"^function LawDef:Deactivate\("),
    ("Lua/Factions/LawDef.lua", r"^function LawDef:EvalDisableConditions\("),
    ("Lua/Factions/LawDef.lua", r"^function PolicyDef:EvalDisableConditions\("),
    ("Lua/Factions/LawDef.lua", r"^function GetPolicyDefaultLaw\("),
    ("Lua/Factions/LawDef.lua", r"^function GetPolicyLaws\("),
    ("Lua/Factions/LawDef.lua", r"^function UpdatePolicyLawCache\("),
    ("Lua/Factions/Legislature.lua", r"^function Legislature:RecalcPoliciesState\("),
    ("Lua/Factions/Legislature.lua", r"^function Legislature:IsPolicyPrepared\("),
    ("Lua/Factions/Legislature.lua", r"^function Legislature:IsActionOnCd\("),
    ("Lua/Factions/Laws.lua", r"^function CheckPoliticalAnimalAchievement\("),
    ("Lua/Factions/Laws.lua", r"^function RevokeLawsDueToConditions\("),
    ("Lua/Buildings/MartianAssembly.lua", r"^function GetMartianAssemblyBuilding\("),
    ("Lua/PreGameMission.lua", r"^function GetCommanderProfile\("),
    ("Lua/Conditions.lua", r"^function FounderStageCompleted:__eval\("),
    ("Lua/Terraforming.lua", r"^function GetAtmosphereBreathable\("),
)

SETUP = r'''
Presets, g_Classes = {}, {}
LawDefs, PolicyDefs, PolicyCategoryDefs = {}, {}, {}
LawDef, PolicyDef, PolicyCategoryDef = {}, {}, {}
Legislature, ScriptProgram, FounderStageCompleted = {}, {}, {}
OnMsg = {}
local CLASS = { LawDef = LawDef, PolicyDef = PolicyDef, PolicyCategoryDef = PolicyCategoryDef }
local MAP = { LawDef = LawDefs, PolicyDef = PolicyDefs, PolicyCategoryDef = PolicyCategoryDefs }
-- property defaults the decision bodies read, from the class definitions:
-- LawDef.lua:5 policy, :17 can_be_repealed, :20 Prerequisite, :21 DisableConditions,
-- :225 Visible, :250 DisableConditions, :252 PreIndependence, :253 PostIndependence,
-- :257 can_be_repealed, :258 CountInAchievementCalc; Preset.lua:85 Obsolete
local DEFAULTS = {
	LawDef = { policy = "", policy_default = false, can_be_repealed = true, Prerequisite = false, DisableConditions = false, Obsolete = false },
	PolicyDef = { PolicyCategory = false, SortKey = 0, PreIndependence = false, PostIndependence = false, can_be_repealed = true,
		CountInAchievementCalc = true, DisableConditions = false, Obsolete = false, SingleLaw = false, custom_cooldown = false },
	PolicyCategoryDef = { Visible = true, SortKey = 0, Obsolete = false },
}
for name, class in pairs(CLASS) do
	class.class = name
	class.__index = class
	setmetatable(class, { __index = DEFAULTS[name] })
	g_Classes[name] = class
	Presets[name] = {}
end
ScriptProgram.__index = ScriptProgram
PRESET_COUNT = { LawDef = 0, PolicyDef = 0, PolicyCategoryDef = 0 }

local function to_props(props)
	if type(props) == "table" and type(props[1]) == "string" and #props % 2 == 0 then
		local t = {}
		for i = 1, #props, 2 do t[props[i]] = props[i + 1] end
		return t
	end
	return props or {}
end

function PlaceObj(classname, props)
	props = to_props(props)
	props.__class = classname
	local class = CLASS[classname]
	if class then
		setmetatable(props, class)
		PRESET_COUNT[classname] = PRESET_COUNT[classname] + 1
		local groups = Presets[classname]
		local gname = props.group or "Default"
		local group = groups[gname]
		if not group then group = { id = gname }; groups[gname] = group; groups[#groups + 1] = group end
		group[#group + 1] = props
		if props.id and group[props.id] == nil then group[props.id] = props end
		if props.id and MAP[classname][props.id] == nil then MAP[classname][props.id] = props end
	elseif classname == "ScriptConditionList" then
		setmetatable(props, { __index = ScriptProgram, __call = function(self, ...) return ScriptProgram.__call(self, ...) end })
	end
	return props
end
function IsKindOf(obj, class) return type(obj) == "table" and (obj.__class == class or rawget(obj, "__is_label_container") and class == "LabelContainer") end
function T(a, b) if type(a) == "table" then return a[1] or "" end return b or a end
function Untranslated(s) return s end
function set(...) local t = {} for _, v in ipairs({...}) do t[v] = true end return t end
function range(a, b) return { a, b } end
function point(...) return { ... } end
function ResolveMap() return nil end
function GameTime() return 0 end
function table.add(t, v) t = t or {}; t[#t + 1] = v; return t end
function table.set(t, ...)
	local n = select("#", ...)
	for i = 1, n - 2 do
		local k = (select(i, ...))
		t[k] = t[k] or {}
		t = t[k]
	end
	t[(select(n - 1, ...))] = (select(n, ...))
end
function table.find_value(t, field, value)
	for _, v in ipairs(t) do if v[field] == value then return v end end
end
function table.remove_value(t, v) for i = #t, 1, -1 do if t[i] == v then table.remove(t, i) return end end end
-- EF-005: engine Lua tolerates #nil and next(nil); LawDef.lua:186 `#disable_explanations` relies on it
debug.setmetatable(nil, { __len = function() return 0 end })
local _next = next
function next(t, k) if type(t) ~= "table" then return nil end return _next(t, k) end

PROCALL_ERRORS = {}
function procall(f, ...)
	local r = table.pack(pcall(f, ...))
	if not r[1] then PROCALL_ERRORS[#PROCALL_ERRORS + 1] = tostring(r[2]) end
	return table.unpack(r, 1, r.n)
end
function dbg() end
function faction_log() end
function AddRevokedLawNotification(law, reason) REVOKED[#REVOKED + 1] = law.id .. ":" .. tostring(reason) end
REVOKED = {}
g_Consts = { LawActionCooldown = 2 * 60 * 1000 }
const = { Scale = { Stat = 1000, h = 60000, sols = 1440000 }, Factions = {} }
UNLOCKS = 0
function AchievementUnlock(id) assert(id == "PoliticalAnimal", id); UNLOCKS = UNLOCKS + 1 end
function Msg(name, ...) if name == "LawActivated" then CheckPoliticalAnimalAchievement() end end
function LawDef:CreateInstance(t) return setmetatable(t, { __index = self }) end
function LawDef:ApplyEffects() end
function LawDef:UnapplyEffects() end
CommanderProfiles = { politician = { id = "politician" }, astrogeologist = { id = "astrogeologist" } }
function GetDefaultCommanderProfile() return CommanderProfiles.astrogeologist end
'''

# The synthetic colony: independent, Martian Assembly built, every policy prepared, and
# every NON-law disable condition already satisfied (2 domes, embassy, sanatorium,
# breathable air, vegetation started, colony goal done, no renegades, founder stage over).
FIXTURE = r'''
function reset_colony(profile)
	MainMap = "MainMap"
	BreathableAtmosphere = true
	Terraforming = { Vegetation = 50 }
	g_ColonyNotViableUntil = -1
	g_Independence = true
	g_AllPoliciesVisibleCheat = false
	Game = { idCommanderProfile = profile or "astrogeologist", game_rules = {}, challenge_id = false }
	local function objs(n) local t = {} for i = 1, n do t[i] = { i = i } end return t end
	UIColony = { __is_label_container = true, labels = {
		MartianAssembly = objs(1), Dome = objs(2), EarthEmbassy = objs(1), Sanatorium = objs(1),
		Renegade = {}, Colonist = objs(50), Founder = {} },
		independence_progress_presets_completed = { colony_goal = true } }
	ActiveLaws = {}
	EnactedInactiveLaws = {}
	g_Legislature = setmetatable({ policies_prepared = {}, last_action_on_preset_id = {} }, { __index = Legislature })
	ForEachPreset("PolicyDef", function(p) g_Legislature.policies_prepared[p.id] = true end)
	UNLOCKS = 0
	REVOKED = {}
end

-- which policies the achievement demands: the shipped state function's output filtered by
-- the three exemption clauses RETYPED from Laws.lua:909-919. Only used to CHOOSE laws; every
-- verdict below is the shipped CheckPoliticalAnimalAchievement's (UNLOCKS), and leg B's
-- positive control + drop-one legs are what hold this retype to the shipped check.
function requirement()
	local req, hidden = {}, {}
	for _, category in ipairs(g_Legislature:RecalcPoliciesState()) do
		for _, pd in ipairs(category) do
			local p = pd.preset
			local exempt = (pd.state == "hidden" and g_Independence and p.PreIndependence)
				or (pd.state == "hidden" and not g_Independence and p.PostIndependence)
				or not p.CountInAchievementCalc
			if not exempt then req[#req + 1] = p.id end
			if pd.state == "hidden" then hidden[p.id] = true end
		end
	end
	return req, hidden
end

function gate_open(law_id)
	local law = LawDefs[law_id]
	return not PolicyDefs[law.policy]:EvalDisableConditions() and not law:EvalDisableConditions()
end

-- one law per required policy; the two Governance picks are the ones Dictatorship needs.
-- EnergyEfficiency takes Power: its Oxygen law is revoked by the next NewDay once Open Domes is
-- active (LawDef-Economy.lua:280 condition, Laws.lua:590-606) -- leg B2 demonstrates it.
PREFER = { Apportionment = "Policy_Apportionment_SingleParty", AssemblyType = "Policy_AssemblyType_Consulting",
	EnergyEfficiency = "Policy_EnergyEfficiency_Power" }
function pick_laws(req)
	local picks = {}
	for _, pid in ipairs(req) do
		local choice = PREFER[pid]
		if not choice then
			for _, law in ipairs(GetPolicyLaws(pid)) do
				if not law:EvalDisableConditions() then choice = law.id break end
			end
		end
		picks[pid] = choice
	end
	return picks
end

-- enact through the voting-card gate only, as many passes as make progress
function enact_honestly(picks, order)
	local pending = {}
	for _, pid in ipairs(order) do pending[#pending + 1] = picks[pid] end
	local progress = true
	while progress do
		progress = false
		for i = #pending, 1, -1 do
			local id = pending[i]
			if id and gate_open(id) then
				LawDefs[id]:Activate()
				table.remove(pending, i)
				progress = true
			end
		end
	end
	return pending
end
'''


def main():
    print("COMMAND python tools/desk_c104_political_animal.py")
    print("HEAD " + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=db.REPO, text=True).strip())
    bench = db.Bench("C104 Political Animal: exclusive laws vs the achievement check; no fix")
    check = bench.check
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS + SETUP)

    files = list(REGISTRIES)
    for pattern in ("Data/LawDef/*.lua", "DLC/norman/Presets/LawDef/*.lua"):
        files += sorted(os.path.relpath(p, db.SRC_LIVE).replace("\\", "/")
                        for p in glob.glob(os.path.join(db.SRC_LIVE, pattern)))
    for rel in files:
        src = db.read(os.path.join(db.SRC_LIVE, rel))
        db.load_at(rt, src, "=" + rel)
        print(f"REGISTRY {rel} sha256={hashlib.sha256(src.encode()).hexdigest()[:16]}")
    for rel, pattern in BODIES:
        text, lo, hi = db.body(rel, pattern)
        db.load_at(rt, text, "=" + rel, lo)
        print(f"SOURCE 1.1.0 {rel}:{lo}-{hi} sha256={hashlib.sha256(text.encode()).hexdigest()[:16]}")
    rt.execute(FIXTURE)
    rt.execute("UpdatePolicyLawCache()")
    g = rt.globals()
    print()

    # ---- A. the instrument reads the registry the extractor read
    counts = g.PRESET_COUNT
    check("registry: 182 LawDef, 87 PolicyDef, 8 PolicyCategoryDef presets loaded (grep count agrees)",
          (counts["LawDef"], counts["PolicyDef"], counts["PolicyCategoryDef"]) == (182, 87, 8),
          (counts["LawDef"], counts["PolicyDef"], counts["PolicyCategoryDef"]))
    rt.execute("reset_colony(); REQ, HIDDEN = requirement()")
    walked = rt.eval("(function() local n = 0 for _, c in ipairs(g_Legislature:RecalcPoliciesState()) do n = n + #c end return n end)()")
    req_n = rt.eval("#REQ")
    check("shipped RecalcPoliciesState walks 67 policies (the static extractor's figure)", walked == 67, walked)
    check("post-independence requirement = 61 policies (66 counted minus 5 hidden PreIndependence)", req_n == 61, req_n)
    for pid in ("NightShiftCompensations", "QualityRest", "SecondaryProduce", "GMO", "EfficientAssembly"):
        g.target = pid
        check(pid + " is in the achievement's requirement set", rt.eval("(function() for _, p in ipairs(REQ) do if p == target then return true end end end)()"))
    check("no procall error while building the requirement (a shim gap would hide a policy)", len(g.PROCALL_ERRORS) == 0,
          list(g.PROCALL_ERRORS.values())[:3])

    # ---- B. positive control: the shipped check CAN unlock, if every requirement is held at once
    rt.execute('''
        reset_colony(); REQ = requirement(); PICKS = pick_laws(REQ)
        LEFT = enact_honestly(PICKS, REQ)
    ''')
    left = sorted(rt.eval("LEFT").values())
    check("honest enactment (voting-card gate only) leaves exactly one law of each exclusive pair un-enactable",
          len(left) == 2 and sum(x in ("Policy_NightShiftCompensations", "Policy_QualityRest") for x in left) == 1
          and sum(x.startswith("Policy_SecondaryProduce_") or x == "Policy_GMO" for x in left) == 1, left)
    check("honest enactment never unlocks the achievement", g.UNLOCKS == 0, g.UNLOCKS)
    rt.execute('for _, id in ipairs(LEFT) do local law = LawDefs[id]; local inst = law:CreateInstance({}); ActiveLaws[#ActiveLaws + 1] = inst; ActiveLaws[id] = inst end')
    rt.execute("RevokeLawsDueToConditions()")
    check("the daily revoke (law-level conditions only) removes nothing from that full set -- both halves of each pair survive",
          len(g.REVOKED) == 0 and rt.eval("ActiveLaws.Policy_NightShiftCompensations and ActiveLaws.Policy_QualityRest and ActiveLaws.Policy_GMO") is not None,
          list(g.REVOKED.values()))
    rt.execute("UNLOCKS = 0; CheckPoliticalAnimalAchievement()")
    check("POSITIVE CONTROL: with the two locked laws forced in (as a cheat would), the revoke-stable set unlocks",
          g.UNLOCKS == 1, g.UNLOCKS)

    # ---- B2. side observation, shipped behaviour: Oxygen is revoked the day Open Domes is active
    rt.execute('''
        reset_colony()
        LawDefs.Policy_EnergyEfficiency_Oxygen:Activate()
        OXY_GATE_AFTER = gate_open("Policy_OpenDomes")
        LawDefs.Policy_OpenDomes:Activate()
        RevokeLawsDueToConditions()
    ''')
    check("B2: Open Domes can still be enacted over Oxygen, and the next NewDay revokes Oxygen (not a blocker: Power/Water remain)",
          rt.eval("OXY_GATE_AFTER") and list(g.REVOKED.values()) == ["Policy_EnergyEfficiency_Oxygen:disable_conditions"]
          and rt.eval("ActiveLaws.Policy_EnergyEfficiency_Oxygen") is None, list(g.REVOKED.values()))
    for law_id in ("Policy_NightShiftCompensations", "Policy_QualityRest", "Policy_GMO"):
        g.target = law_id
        rt.execute("local inst = ActiveLaws[target]; table.remove_value(ActiveLaws, inst); ActiveLaws[target] = nil; UNLOCKS = 0; CheckPoliticalAnimalAchievement(); ActiveLaws[#ActiveLaws + 1] = inst; ActiveLaws[target] = inst")
        check("REQUIREMENT: dropping " + law_id + " from that full set refuses the unlock", g.UNLOCKS == 0, g.UNLOCKS)

    # ---- C. both enactment orders of both pairs are refused by the shipped conditions
    pairs = (("Policy_NightShiftCompensations", "Policy_QualityRest"),
             ("Policy_SecondaryProduce_Herbs", "Policy_GMO"),
             ("Policy_SecondaryProduce_Spices", "Policy_GMO"),
             ("Policy_SecondaryProduce_Sugar", "Policy_GMO"))
    for a, b in pairs:
        for first, second in ((a, b), (b, a)):
            g.first, g.second = first, second
            ok = rt.eval('''(function()
                reset_colony()
                if not gate_open(first) then return "first locked" end
                LawDefs[first]:Activate()
                return gate_open(second) and "second OPEN" or "second locked"
            end)()''')
            check(f"order {first} then {second}: second is locked", ok == "second locked", ok)

    # ---- D. every law-on-law lock among the requirement set, enumerated from the shipped bodies
    edges = rt.eval(r'''(function()
        reset_colony(); local req = requirement(); local edges = {}
        local function fully_locked(pid)
            if PolicyDefs[pid]:EvalDisableConditions() then return true end
            for _, law in ipairs(GetPolicyLaws(pid)) do if not law:EvalDisableConditions() then return false end end
            return true
        end
        for _, target in ipairs(req) do
            for _, other in ipairs(req) do
                if other ~= target then
                    for _, law in ipairs(GetPolicyLaws(other)) do
                        ActiveLaws = {}
                        local before = fully_locked(target)
                        local inst = law:CreateInstance({}); ActiveLaws[1] = inst; ActiveLaws[law.id] = inst
                        if not before and fully_locked(target) then edges[#edges + 1] = law.id .. " locks " .. target end
                    end
                end
            end
        end
        table.sort(edges)
        return table.concat(edges, "\n")
    end)()''')
    edge_list = [e for e in edges.split("\n") if e]
    print("  LOCK EDGES (an active law that fully locks a required policy):")
    for e in edge_list:
        print("     " + e)
    expected = {
        "Dictatorship locks Apportionment", "Dictatorship locks AssemblyType",
        "Policy_NightShiftCompensations locks QualityRest", "Policy_QualityRest locks NightShiftCompensations",
        "Policy_GMO locks SecondaryProduce",
        "Policy_SecondaryProduce_Herbs locks GMO", "Policy_SecondaryProduce_Spices locks GMO", "Policy_SecondaryProduce_Sugar locks GMO",
    }
    check("the lock graph is exactly: 2 mutual pairs + Dictatorship's one-way lock (resolved by enacting it last)",
          set(edge_list) == expected, sorted(set(edge_list) ^ expected))
    check("no procall error across the enumeration", len(g.PROCALL_ERRORS) == 0, list(g.PROCALL_ERRORS.values())[:3])

    # ---- E. the Politician commander: a second, independent blocker
    rt.execute("reset_colony('politician'); REQ_P, HIDDEN_P = requirement()")
    check("Politician: shipped state function marks EfficientAssembly hidden",
          rt.eval("HIDDEN_P.EfficientAssembly") is True)
    check("Politician: EfficientAssembly is still required (hidden but not exempt)",
          rt.eval("(function() for _, p in ipairs(REQ_P) do if p == 'EfficientAssembly' then return true end end end)()") is True)
    rt.execute("reset_colony('astrogeologist'); REQ_A, HIDDEN_A = requirement()")
    check("control: any other commander sees EfficientAssembly unhidden", not rt.eval("HIDDEN_A.EfficientAssembly"))
    rt.execute('''
        reset_colony('politician'); REQ_P = requirement(); PICKS = pick_laws(REQ_P)
        PICKS.EfficientAssembly = nil
        LEFT = enact_honestly(PICKS, REQ_P)
        for _, id in ipairs(LEFT) do local inst = LawDefs[id]:CreateInstance({}); ActiveLaws[#ActiveLaws + 1] = inst; ActiveLaws[id] = inst end
        UNLOCKS = 0; CheckPoliticalAnimalAchievement()
    ''')
    check("Politician: even with both pairs forced in, the unlock is refused (EfficientAssembly unreachable)",
          g.UNLOCKS == 0, g.UNLOCKS)

    # ---- F. fix-shape probe (NOT a recommendation): the shipped check needs only a data flag
    rt.execute('''
        PolicyDefs.QualityRest.CountInAchievementCalc = false
        PolicyDefs.GMO.CountInAchievementCalc = false
        reset_colony(); REQ = requirement(); PICKS = pick_laws(REQ); LEFT = enact_honestly(PICKS, REQ)
        HONEST_UNLOCKS = UNLOCKS
        PolicyDefs.EfficientAssembly.CountInAchievementCalc = false
        reset_colony('politician'); REQ = requirement(); PICKS = pick_laws(REQ); LEFT_P = enact_honestly(PICKS, REQ)
        POLITICIAN_UNLOCKS = UNLOCKS
        PolicyDefs.QualityRest.CountInAchievementCalc = true
        PolicyDefs.GMO.CountInAchievementCalc = true
        PolicyDefs.EfficientAssembly.CountInAchievementCalc = true
    ''')
    check("fix shape: exempting one policy of each pair lets HONEST enactment unlock (Astrogeologist)",
          g.HONEST_UNLOCKS >= 1 and len(rt.eval("LEFT")) == 0, (g.HONEST_UNLOCKS, len(rt.eval("LEFT"))))
    check("fix shape: plus exempting EfficientAssembly lets a Politician unlock honestly",
          g.POLITICIAN_UNLOCKS >= 1 and len(rt.eval("LEFT_P")) == 0, (g.POLITICIAN_UNLOCKS, len(rt.eval("LEFT_P"))))
    check("no procall error in any leg", len(g.PROCALL_ERRORS) == 0, list(g.PROCALL_ERRORS.values())[:3])

    return bench.finish("CONTROLS HOLD: on 1.1.0 no normal-play enactment order satisfies the shipped Political Animal check.")


if __name__ == "__main__":
    sys.exit(main())
