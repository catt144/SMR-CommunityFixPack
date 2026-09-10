#!/usr/bin/env python3
"""Desk falsifier for C74/C77's seven-unit animation-moment repair.

The relevant shipped 1.1.0 bodies are extracted with tools/luafn and loaded
under their real file names and line offsets. The module is loaded whole. The
only retyped pieces are named engine shims and fixtures around those bodies.

Demands:
  L0  shipped numeric lookup misses a known name-keyed marker
  L1  module conversion makes that numeric lookup find the marker
  L2  a future resolved lookup makes the conversion guard decline
  L3  an existing group/id wins and a second data-ready pass adds nothing
  L4  the Excavator's 24 moments are time-sorted and keep every exact type
  L5  old-save pass replaces one vanilla tracker for each long-lived unit
  L6  a second load pass still leaves exactly one replacement per unit
  L7  Water Extractor update deletes/replaces its early tracker exactly once
  L8  the shared defect probe also applies on the archived 1.0.7 bodies
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402


PRELUDE = db.ENGINE_SHIMS + r'''
function table.ifilter(t, fn, arg)
	local out = {}
	for _, v in ipairs(t) do if fn(v, arg) then out[#out + 1] = v end end
	return out
end
function table.find(t, key, value)
	for i, v in ipairs(t) do if type(v) == "table" and v[key] == value then return i end end
end
function MulDivRound(a, b, c) return math.floor(a * b / c + 0.5) end
function GetStateIdx(name) return name == "working" and 20 or -1 end
function GetStateName(idx) return idx == 20 and "working" or tostring(idx) end
function GetAnimEntity(entity, anim) return entity end
function IsValid(o) return type(o) == "table" and o.valid ~= false end
function IsKindOf(o, class) return type(o) == "table" and o._kind == class end
function IsValidThread(t) return type(t) == "table" and t.alive == true end
function DeleteThread(t) if type(t) == "table" then t.alive = false end end
function CreateGameTimeThread(fn, ...) return { alive = true, fn = fn, args = {...} } end

Presets = { AnimMetadata = {} }
PLACED = 0
function PlaceObj(class, data)
	if class ~= "AnimMetadata" then return data end
	local groups = Presets.AnimMetadata
	local group = groups[data.group]
	if not group then group = {}; groups[data.group] = group; groups[#groups + 1] = group end
	group[#group + 1] = data
	group[data.id] = data
	PLACED = PLACED + 1
	return data
end

OnMsg = {}
LOGS = {}
DATA_READY = false
SMRFixPack_Disabled = {}
SMRFixPack = { fixes = {} }
function SMRFixPack.Log(fmt, ...)
	LOGS[#LOGS + 1] = string.format(fmt, ...)
end
function SMRFixPack.IsActive(id)
	local f = SMRFixPack.fixes[id]
	return f and f.status == "active"
end
function SMRFixPack.WhenActive(id, fn)
	return function(...)
		if not SMRFixPack.IsActive(id) or SMRFixPack_Disabled[id] then return end
		return fn(...)
	end
end
function SMRFixPack.OnDataReady(fn) DATA_READY = fn end
function SMRFixPack.Require(id, spec)
	for _, c in ipairs(spec) do
		local ok = false
		if c.probe then
			local pok, result = pcall(c.probe)
			ok = pok and result == true
		elseif c.global then
			local v = rawget(_G, c.global)
			ok = type(v) == (c.kind or "function")
		elseif c.class and c.method then
			local cls = rawget(_G, c.class)
			ok = type(cls) == "table" and type(cls[c.method]) == "function"
		end
		if not ok then return c.reason or "declined" end
	end
end
function SMRFixPack.Register(id, def)
	local entry = { status = "pending", detail = "" }
	SMRFixPack.fixes[id] = entry
	local ok, result = pcall(def.apply)
	if not ok then entry.status = "error"; entry.detail = tostring(result)
	elseif type(result) == "string" then entry.status = "inactive"; entry.detail = result
	else entry.status = "active" end
end

CObject = {}
BaseBuilding = {}
POPULATION = {}
function AllMapsForEach(_, class, fn)
	for _, obj in ipairs(POPULATION[class] or {}) do fn(obj) end
end
'''


SHIPPED = [
    ("CommonLua/Classes/AnimMoment.lua", [
        r"^function GetEntityAnimMoments\(",
        r"^function CObject:GetAnimMoments\(",
    ], "span"),
    ("CommonLua/Classes/AnimMoment.lua", r"^function CObject:GetAnimMomentsCount\(", "body"),
    ("Lua/Buildings/BaseBuilding.lua", r"^function BaseBuilding:UpdateWorkingStateAnim\(", "body"),
    ("Lua/Buildings/BaseBuilding.lua", r"^function BaseBuilding:TrackMultipleHitMoments\(", "body"),
    ("Lua/Buildings/Building.lua", [
        r"^function GetAllAnimMoments\(",
        r"^function TrackAllMoments\(",
    ], "span"),
]


def runtime(get_override=None, tree="1.1.0"):
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    spans = []
    for rel, pattern, kind in SHIPPED:
        if kind == "span":
            text, start, end = db.span(rel, pattern, tree=tree)
        else:
            text, start, end = db.body(rel, pattern, tree=tree)
        db.load_at(rt, text, "=" + rel, start)
        spans.append((rel, start, end))
    if get_override:
        rt.execute(get_override)
    db.load_at(rt, db.read(os.path.join(db.REPO, "Code", "Fix_SilentHitMomentFX.lua")),
               "=Code/Fix_SilentHitMomentFX.lua")
    return rt, spans


def main():
    bench = db.Bench("C74/C77 silent hit-moment FX -- shipped bodies + whole module")
    expect = bench.check

    # Vanilla control before the module is loaded.
    rt0 = db.lua_runtime()
    rt0.execute(PRELUDE)
    text, start, _ = db.span("CommonLua/Classes/AnimMoment.lua", [
        r"^function GetEntityAnimMoments\(", r"^function CObject:GetAnimMoments\("])
    db.load_at(rt0, text, "=CommonLua/Classes/AnimMoment.lua", start)
    rt0.execute(r'''
	Presets.AnimMetadata.UniversalExtractorHammer = {
		working = { Moments = { { Type = "Hit", Time = 1 } } }
	}
	PROBE_OBJ = { _kind = "UniversalExtractorHammer", GetEntity = function() return "UniversalExtractorHammer" end,
		GetStateText = function() return "working" end }
	VANILLA_NAME = #CObject.GetAnimMoments(PROBE_OBJ, "working")
	VANILLA_INDEX = #CObject.GetAnimMoments(PROBE_OBJ, 20)
''')
    expect("[L0] shipped lookup finds the name but misses its numeric index",
           (rt0.globals().VANILLA_NAME, rt0.globals().VANILLA_INDEX) == (1, 0),
           f"name/index={rt0.globals().VANILLA_NAME}/{rt0.globals().VANILLA_INDEX}")

    rt, spans = runtime()
    for rel, start, end in spans:
        print(f"extracted {rel}:{start}-{end}")
    g = rt.globals()
    expect("[setup] current shipped lookup shape applies the module",
           g.SMRFixPack.fixes["SilentHitMomentFX"].status == "active",
           g.SMRFixPack.fixes["SilentHitMomentFX"].detail)

    # Existing preset must win. The callback adds the other ten entries.
    rt.execute(r'''
	SENTINEL = { group = "Shuttle", id = "landing", Moments = { { Type = "Keep", Time = 7 } } }
	PlaceObj("AnimMetadata", SENTINEL)
	local before = PLACED
	DATA_READY()
	ADDED_FIRST = PLACED - before
	local after = PLACED
	DATA_READY()
	ADDED_SECOND = PLACED - after
	SENTINEL_KEPT = Presets.AnimMetadata.Shuttle.landing == SENTINEL
	PROBE_OBJ = { _kind = "UniversalExtractorHammer", GetEntity = function() return "UniversalExtractorHammer" end,
		GetStateText = function() return "working" end }
	INDEX_AFTER = #CObject.GetAnimMoments(PROBE_OBJ, 20, "Hit")
	FOREIGN_PROBE_OBJ = { _kind = "Foreign", GetEntity = function() return "UniversalExtractorHammer" end,
		GetStateText = function() return "working" end }
	FOREIGN_INDEX_AFTER = #CObject.GetAnimMoments(FOREIGN_PROBE_OBJ, 20, "Hit")
''')
    expect("[L1] conversion resolves the two owned attach classes and leaves a foreign object inert",
           g.INDEX_AFTER == 2 and g.FOREIGN_INDEX_AFTER == 0,
           f"owned/foreign={g.INDEX_AFTER}/{g.FOREIGN_INDEX_AFTER}")
    expect("[L3] existing group/id wins; first pass adds ten and second adds zero",
           g.ADDED_FIRST == 10 and g.ADDED_SECOND == 0
           and bool(g.SENTINEL_KEPT),
           f"added={g.ADDED_FIRST}/{g.ADDED_SECOND}, kept={g.SENTINEL_KEPT}")

    rt.execute(r'''
	local m = Presets.AnimMetadata.ExcavatorShovel.working.Moments
	EX_COUNT, EX_SORTED = #m, true
	EX_TYPES = {}
	for i, x in ipairs(m) do
		if i > 1 and x.Time < m[i - 1].Time then EX_SORTED = false end
		EX_TYPES[x.Type] = (EX_TYPES[x.Type] or 0) + 1
	end
	for i = 1, 12 do
		if EX_TYPES["Hit" .. i] ~= 1 or EX_TYPES["Out" .. i] ~= 1 then EX_SORTED = false end
	end
''')
    expect("[L4] Excavator has 24 sorted moments and each Hit/Out type exactly once",
           g.EX_COUNT == 24 and bool(g.EX_SORTED), f"count={g.EX_COUNT}")

    # Replace the vanilla starter with an observable engine stub only AFTER the
    # shipped body was loaded and the module captured everything it wraps.
    rt.execute(r'''
	START_ALL, START_MULTI = 0, 0
	function TrackAllMoments(obj, action, actor, target)
		START_ALL = START_ALL + 1
		return { alive = true, action = action }
	end
	local function part(entity)
		return setmetatable({ entity = entity, speed = 1000, valid = true, _kind = entity }, { __index = {
			GetEntity = function(self) return self.entity end,
			GetStateText = function() return "working" end,
			GetAnim = function() return 20 end,
			GetAnimSpeed = function(self) return self.speed end,
			HasEntity = function() return true end,
			HasAnim = function(_, anim) return anim == "working" end,
			GetAnimMoments = CObject.GetAnimMoments,
			GetAnimMomentsCount = CObject.GetAnimMomentsCount,
		} })
	end
	local function building(entity, class)
		local p = part(entity)
		return {
			working = true, work_anim_loop = "working", _kind = class,
			track_multiple_hit_moments_in_work_state = true,
			GetAttaches = function() return { p } end,
			TrackMultipleHitMoments = function(self)
				START_MULTI = START_MULTI + 1
				DeleteThread(self.track_multiple_hit_thread)
				self.track_multiple_hit_thread = { alive = true }
			end,
			HasEntity = function() return true end,
			HasAnim = function() return false end,
			GetAttach = function(_, wanted) if wanted == "WaterExtractorPump" then return p end end,
			part = p,
		}
	end
	local hammer = building("UniversalExtractorHammer", "PreciousMetalsExtractor")
	local moxie = building("MoxiePump", "MOXIEBase")
	local water = building("WaterExtractorPump", "WaterExtractorBase")
	local excavator = building("unused", "TheExcavatorBase")
	excavator.arm = part("ExcavatorShovel")
	excavator.dig_anim_thread = { alive = true }
	hammer.track_multiple_hit_thread = { alive = true }
	moxie.track_multiple_hit_thread = { alive = true }
	water.anim_moments_thread = { alive = true }
	excavator.dig_fx_thread = { alive = true }
	HAMMER_OLD = hammer.track_multiple_hit_thread
	MOXIE_OLD = moxie.track_multiple_hit_thread
	WATER_LOAD_OLD = water.anim_moments_thread
	EXCAVATOR_OLD = excavator.dig_fx_thread
	POPULATION = {
		PreciousMetalsExtractor = { hammer }, MOXIEBase = { moxie },
		WaterExtractorBase = { water }, TheExcavatorBase = { excavator },
	}
	OnMsg.LoadGame()
	LOAD_FIRST_ALL, LOAD_FIRST_MULTI = START_ALL, START_MULTI
	LOAD_FIRST_REPLACED = not HAMMER_OLD.alive and not MOXIE_OLD.alive
		and not WATER_LOAD_OLD.alive and not EXCAVATOR_OLD.alive
	HAMMER_FIRST = hammer.track_multiple_hit_thread
	MOXIE_FIRST = moxie.track_multiple_hit_thread
	WATER_FIRST = water.anim_moments_thread
	EXCAVATOR_FIRST = excavator.dig_fx_thread
	OnMsg.LoadGame()
	LOAD_SECOND_ALL, LOAD_SECOND_MULTI = START_ALL, START_MULTI
	LOAD_SECOND_REPLACED = not HAMMER_FIRST.alive and not MOXIE_FIRST.alive
		and not WATER_FIRST.alive and not EXCAVATOR_FIRST.alive
	LOAD_SECOND_LIVE = IsValidThread(hammer.track_multiple_hit_thread)
		and IsValidThread(moxie.track_multiple_hit_thread)
		and IsValidThread(water.anim_moments_thread)
		and IsValidThread(excavator.dig_fx_thread)

	WATER_OLD = { alive = true }
	water.anim_moments_thread = WATER_OLD
	water.part.speed = 0
	water.ChangeWorkingStateAnim = function(self) self.part.speed = 1000 end
	BaseBuilding.UpdateWorkingStateAnim(water)
	WATER_REPLACED = (not WATER_OLD.alive) and IsValidThread(water.anim_moments_thread)
	WATER_AFTER_ALL = START_ALL

	FOREIGN_CALLS = 0
	local foreign = { _kind = "Foreign", ChangeWorkingStateAnim = function() FOREIGN_CALLS = FOREIGN_CALLS + 1 end }
	BaseBuilding.UpdateWorkingStateAnim(foreign)
''')
    expect("[L5] old-save pass replaces exactly four apparently-live vanilla trackers",
           g.LOAD_FIRST_ALL == 2 and g.LOAD_FIRST_MULTI == 2
           and bool(g.LOAD_FIRST_REPLACED),
           f"TrackAll/Multi={g.LOAD_FIRST_ALL}/{g.LOAD_FIRST_MULTI}, replaced={g.LOAD_FIRST_REPLACED}")
    expect("[L6] each load pass replaces rather than adds, leaving one live tracker per unit",
           g.LOAD_SECOND_ALL == 4 and g.LOAD_SECOND_MULTI == 4
           and bool(g.LOAD_SECOND_REPLACED) and bool(g.LOAD_SECOND_LIVE),
           f"after second={g.LOAD_SECOND_ALL}/{g.LOAD_SECOND_MULTI}, replaced={g.LOAD_SECOND_REPLACED}, live={g.LOAD_SECOND_LIVE}")
    expect("[L7] Water update deletes/replaces one early tracker; foreign object passes through",
           bool(g.WATER_REPLACED) and g.WATER_AFTER_ALL == g.LOAD_SECOND_ALL + 1 and g.FOREIGN_CALLS == 1,
           f"TrackAll={g.WATER_AFTER_ALL}, foreign={g.FOREIGN_CALLS}")

    # Future-dev control: a name-resolving body is left installed, not wrapped.
    fixed = r'''
	function CObject:GetAnimMoments(anim, moment_type)
		if type(anim) == "number" then anim = GetStateName(anim) end
		return GetEntityAnimMoments(self:GetEntity(), anim or self:GetStateText(), moment_type)
	end
	FIXED_GET = CObject.GetAnimMoments
'''
    rt2, _ = runtime(fixed)
    g2 = rt2.globals()
    rt2.execute("FIXED_GET_KEPT = CObject.GetAnimMoments == FIXED_GET")
    expect("[L2] resolved future lookup makes the conversion guard decline cleanly",
           g2.SMRFixPack.fixes["SilentHitMomentFX"].status == "active"
           and bool(g2.FIXED_GET_KEPT),
           f"{g2.SMRFixPack.fixes['SilentHitMomentFX'].detail}; kept={g2.FIXED_GET_KEPT}")

    rt3, _ = runtime(tree="1.0.7")
    g3 = rt3.globals()
    rt3.execute(r'''
	DATA_READY()
	OLD_OBJ = { _kind = "UniversalExtractorHammer", GetEntity = function() return "UniversalExtractorHammer" end,
		GetStateText = function() return "working" end }
	OLD_INDEX_AFTER = #CObject.GetAnimMoments(OLD_OBJ, 20, "Hit")
''')
    expect("[L8] archived 1.0.7 bodies expose the same defect and take the shared repair",
           g3.SMRFixPack.fixes["SilentHitMomentFX"].status == "active" and g3.OLD_INDEX_AFTER == 2,
           f"status={g3.SMRFixPack.fixes['SilentHitMomentFX'].status}, moments={g3.OLD_INDEX_AFTER}")

    return bench.finish("ALL DEMANDS HELD -- current defect, future decline, preset guards, load repair and Water replacement discriminate.")


if __name__ == "__main__":
    sys.exit(main())
