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
        const = {TechPointResearchCost = 1}; g_TechTimesResearched = {}
        g_ForceTechRepeatable = false
        function T(_, text) return text end
        function point(...) return {...} end
        function set(...) return {...} end
        function PlaceObj(class, props)
            if class == "Tech" then
                setmetatable(props, {__index = {CanBeResearched = true, Repeatable = false, save_in = "", EffectsApply = function() end}})
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
        function RemoveTechLockReason() end -- fixture techs are already enabled
        function ResearchQueue:DequeueTech() end -- no queue in this fixture
        function CountResearchedTech() end
        function LogResearchedTech() end
        function Msg(name, ...) if name == "TechResearched" then OnMsg.TechResearched(...) end end
        function IsTechDiscounted() return false end -- after the achievement event
        function procall() end -- post-event research effects not modelled
        function ObjModified() end
        function CheckLockPrerequisites() end -- post-event lock updates not modelled
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
        ("CommonLua/Libs/Research/Research.lua", r"^function UnhideTech\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function UnlockTech\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function ResearchTech\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function ResearchQueue:ResearchTech\("),
        ("Lua/TechTree.lua", r"^function Player:IsTechResearched\("),
        ("Lua/Tech.lua", r"^function IsTechResearched\("),
        ("Lua/Tech.lua", r"^function IsTechRepeatable\("),
        ("Lua/TechTree.lua", r"^function Player:CanResearch\("),
        ("Lua/TechTree.lua", r"^function Player:UIResearch\("),
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
    db.load_at(rt, prefix + "\nc92_filter = IsCountedForResearchedAllTechsAchievement; c92_groups = researched_all_techs", "=Lua/Achievements.lua")
    rt.execute(r'''
        setmetatable(Player, {__index = ResearchQueue})
        UIPlayer = setmetatable({tech_researched = {}, tech_research_points = {}, TechPoints = 3}, {__index = Player})
        UIColony = setmetatable({day = 490}, {__index = Research})
        for id in pairs(Techs) do UIPlayer.tech_researched[id] = true end
    ''')
    check = bench.check
    rt.execute('''
        UIPlayer.tech_researched.MartianCopyrithgts = nil
        UIPlayer.tech_researched.MartianPatents = nil
        assert(UIPlayer:UIResearch("MartianCopyrithgts"))
    ''')
    check("first repeatable completion writes researched before achievement check",
          rt.eval('IsTechResearched("MartianCopyrithgts") and g_TechTimesResearched.MartianCopyrithgts == 1') and rt.globals().unlocks == 0)
    rt.execute('assert(UIPlayer:UIResearch("MartianPatents"))')
    check("second repeatable first completion permits the vanilla achievement request", rt.globals().unlocks == 1)
    rt.execute('unlocks = 0; assert(UIPlayer:UIResearch("MartianPatents"))')
    check("repeat research succeeds without clearing its completed state",
          rt.eval('IsTechResearched("MartianPatents") and g_TechTimesResearched.MartianPatents == 2') and rt.globals().unlocks == 0)
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
        g_ForceTechRepeatable = false
        UIPlayer.tech_researched.UndergroundExploitation = nil
        unlocks = 0
        OnMsg.TechResearched("MartianPatents", UIColony, true)
        function all_groups(filter)
            for _, id in ipairs(c92_groups) do
                if not UIColony:IsTechGroupResearched(id, filter) then return false end
            end
            return true
        end
        function exclude_repeatables(tech, group)
            return c92_filter(tech, group) and not UIColony:IsTechRepeatable(tech.id)
        end
        function exclude_orphan(tech, group)
            return c92_filter(tech, group) and tech.id ~= "UndergroundExploitation"
        end
    ''')
    check("actual hidden preset UndergroundExploitation is counted and blocks unlock",
          rt.eval('Techs.UndergroundExploitation.LockState == "hidden" and not Techs.UndergroundExploitation.Obsolete and c92_filter(Techs.UndergroundExploitation)') and rt.globals().unlocks == 0)
    check("excluding repeatables still fails with the orphan unresearched", not rt.eval('all_groups(exclude_repeatables)'))
    check("excluding only the orphan permits all complete groups", rt.eval('all_groups(exclude_orphan)'))
    rt.execute('UIPlayer.tech_researched.MartianPatents = nil')
    check("orphan-only exclusion retains the repeatable first-completion requirement", not rt.eval('all_groups(exclude_orphan)'))
    rt.execute('UIPlayer.tech_researched.MartianPatents = true')
    # Choose a real counted ordinary tech rather than manufacturing one.
    rt.execute('''
        ordinary = nil
        for _, group_id in ipairs(c92_groups) do
            ForEachPresetInGroup("TechGroup", group_id, function(cluster)
                ForEachPresetInGroup("Tech", cluster.id, function(tech)
                    if c92_filter(tech) and not tech.Repeatable and tech.id ~= "UndergroundExploitation" then ordinary = tech.id; return "break" end
                end)
            end)
        end
        assert(ordinary); UIPlayer.tech_researched[ordinary] = nil
    ''')
    check("orphan-only exclusion still refuses an incomplete ordinary counted tech", not rt.eval('all_groups(exclude_orphan)'))
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
