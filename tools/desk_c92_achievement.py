#!/usr/bin/env python3
"""C92 investigation: execute shipped registry, state, and achievement bodies.

No fix module is loaded or built. PlaceObj stores property tables with the
shipped Tech defaults; presentation constructors are inert. Research-state
decisions, preset iteration and achievement filtering are extracted verbatim.
The unlock sink observes a request and never contacts Steam. Synthetic player
state is explicit; this is not a reproduction of the supplied save.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

import deskbench as db


def install(rt, rel, pattern):
    text, lo, hi = db.body(rel, pattern)
    db.load_at(rt, text, "=" + rel, lo)
    print(f"SOURCE 1.1.0.403908 {rel}:{lo}-{hi} sha256={hashlib.sha256(text.encode()).hexdigest()}")


def main():
    print("COMMAND python tools/desk_c92_achievement.py")
    print("HEAD " + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=db.REPO, text=True).strip())
    bench = db.Bench("C92 achievement hypothesis controls; no fix")
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS + r'''
        Presets = {Tech = {}, TechGroup = {}}
        Techs = {}; TechGroups = {}; empty_table = {}
        Research = {}; ResearchQueue = {}; Player = {}; OnMsg = {}
        g_ForceTechRepeatable = false
        function T(_, text) return text end
        function point(...) return {...} end
        function set(...) return {...} end
        function PlaceObj(class, props)
            if class == "Tech" then
                setmetatable(props, {__index = {CanBeResearched = true, Repeatable = false, save_in = ""}})
                Techs[props.id] = props
            elseif class == "TechGroup" then TechGroups[props.id] = props
            else return props end
            local list = Presets[class][props.group] or {}
            Presets[class][props.group] = list
            list[#list + 1] = props; list[props.id] = props
            return props
        end
        function GetDefaultResearchQueue() return UIPlayer end
        function GetPresetLockStateAndText(tech) return tech.LockState or "enabled" end
        function GetMissionSponsor() return {id = "Japan"} end
        function GetAchievementFlags() return false end
        unlocks = 0
        function AchievementUnlock(id) assert(id == "ResearchedAllTechs"); unlocks = unlocks + 1 end
        function table.findfirst(t, fn, ...)
            for i, entry in ipairs(t) do if fn(i, entry, ...) then return i end end
        end
        function IsResearchQueueEntryAResearch(entry) return entry.kind == "research" end
    ''')
    for rel in ("Data/TechGroup.lua", "Data/Tech.lua"):
        src = db.read(Path(db.SRC_LIVE) / rel)
        db.load_at(rt, src, "=" + rel)
        print(f"REGISTRY {rel} sha256={hashlib.sha256(src.encode()).hexdigest()}")
    for rel, pattern in (
        ("CommonLua/Preset.lua", r"^function ForEachPresetInGroup\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function ResearchQueue:IsTechResearched\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function IsResearched\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function GetTechState\("),
        ("Lua/TechTree.lua", r"^function Player:IsTechResearched\("),
        ("Lua/Tech.lua", r"^function IsTechResearched\("),
        ("Lua/TechTree.lua", r"^function IsInitiative\("),
        ("Lua/Research.lua", r"^function Research:IsTechRepeatable\("),
        ("Lua/Research.lua", r"^function Research:IsTechResearched\("),
        ("Lua/Research.lua", r"^function Research:IsTechDiscoverable\("),
        ("Lua/Research.lua", r"^function Research:IsTechClusterResearched\("),
        ("Lua/Research.lua", r"^function Research:IsTechGroupResearched\("),
    ):
        install(rt, rel, pattern)
    achievement = db.read(Path(db.SRC_LIVE) / "Lua/Achievements.lua")
    prefix = achievement[:achievement.index("function OnMsg.ConstructionComplete")]
    db.load_at(rt, prefix, "=Lua/Achievements.lua")
    rt.execute(r'''
        UIPlayer = setmetatable({tech_researched = {}}, {__index = Player})
        UIColony = setmetatable({day = 490}, {__index = Research})
        for id in pairs(Techs) do UIPlayer.tech_researched[id] = true end
    ''')
    check = bench.check
    for tech_id in ("MartianCopyrithgts", "MartianPatents"):
        rt.globals().target = tech_id
        check(tech_id + " remains researched with Repeatable=true",
              rt.eval('Techs[target].Repeatable and IsTechResearched(target) and GetTechState(target) == "researched"'))
    rt.execute('OnMsg.TechResearched("MartianPatents", UIColony, true)')
    check("vanilla achievement requests unlock when all counted techs are researched", rt.globals().unlocks == 1)
    rt.execute('unlocks = 0; OnMsg.TechResearched("MartianPatents", UIColony, false)')
    check("repeat completions do not retry achievement (first_time gate)", rt.globals().unlocks == 0)
    rt.execute('UIPlayer.tech_researched.MartianPatents = nil; OnMsg.TechResearched("MartianCopyrithgts", UIColony, true)')
    check("a repeatable never completed once legitimately prevents unlock", rt.globals().unlocks == 0)
    rt.execute('''
        UIPlayer.tech_researched.MartianPatents = true
        UIPlayer.tech_researched.MartianCopyrithgts = nil
        UIPlayer.TechnologiesUndoQueue = {{tech_id = "MartianCopyrithgts", kind = "research"}}
        OnMsg.TechResearched("MartianPatents", UIColony, true)
    ''')
    check("preview research can also satisfy the vanilla state check", rt.globals().unlocks == 1)
    rt.execute('UIPlayer.TechnologiesUndoQueue = nil; UIPlayer.tech_researched.MartianCopyrithgts = true')
    rt.execute('''
        g_ForceTechRepeatable = {MartianPatents = false}
    ''')
    check("effective repeatability can disagree with preset Repeatable", not rt.eval('UIColony:IsTechRepeatable("MartianPatents")') and rt.eval('Techs.MartianPatents.Repeatable'))
    rt.execute('''
        function report(tech)
            if tech.Repeatable then
                local group = TechGroups[tech.group]
                print("REPEATABLE " .. tech.id .. " cluster=" .. tech.group .. " group=" .. tostring(group and group.group) .. " save_in=" .. tech.save_in)
            end
        end
        for _, tech in pairs(Techs) do report(tech) end
    ''')
    return bench.finish("CONTROLS HOLD: repeatables retain completion; unconditional exemption changes the achievement requirement.")


if __name__ == "__main__":
    sys.exit(main())
