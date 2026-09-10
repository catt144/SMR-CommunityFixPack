#!/usr/bin/env python3
"""Vanillahunt 03c source controls; no game, mod, or archive writes.

Executes shipped FactionsHolder/Legislature bodies with explicit Lua shims.
It also checks the live 1.1.0 DeepScanning registry/consumer route and the
first-session popup's literal route. It does not emulate native persistence,
scheduling, UI behavior, or dynamic/native dispatch.
"""
from pathlib import Path

import deskbench as d


ARCHIVE = Path(d.SRC_ARCHIVE).parent.parent
for version, folder in (("1.0.7", "1.0.7.396349"), ("1.1.0", "1.1.0.403908")):
    d.TREES[version] = str(ARCHIVE / folder / "Src")


def install(rt, rel, name, version):
    text, first, _ = d.body(rel, r"^function " + name + r"\(", version)
    d.load_at(rt, text, "=" + rel, first)


def disaster(version, seats):
    rt = d.lua_runtime()
    rt.execute("""
        FactionsHolder = {}
        const = {DayDuration = 1000}
        UIColony = {labels = {FactionObject = {}}}
        FactionDefs = {A = {DisasterThreshold = 500, DisasterType = 'Fixture'}}
        g_Classes = {}
        g_Legislature = {legislature_members = {A = fixture_seats}}
        messages = {}; updates = 0
        function GameTime() return 1000 end
        function faction_log(...) return '' end
        function dbg(...) end
        function Msg(name, ...) messages[#messages + 1] = name end
        function ShowPopupNotification(...) end
        function TList(...) return '' end
    """)
    rt.globals().fixture_seats = seats
    # The table above was created before fixture_seats was assigned; set the
    # member explicitly so false/zero remains representable.
    rt.execute("g_Legislature.legislature_members.A = fixture_seats")
    rel = "Lua/Factions/Factions.lua"
    install(rt, rel, "FactionsHolder:RecalcFactionsDisasters", version)
    install(rt, rel, "FactionsHolder:UpdateFactionsDisasters", version)
    return rt.execute("""
        local disaster = {
            faction_id = 'A', start_time = 0, max_duration = 100,
            ShouldStop = function() return false end,
            DailyUpdate = function() updates = updates + 1 end,
        }
        local holder = setmetatable({
            active_factions = {A = true}, factions_tension = {A = 900},
            factions_tension_warnings = {A = true},
            factions_approval = {A = {approval = -1000}},
            factions_disaster = {A = disaster},
        }, {__index = FactionsHolder})
        holder:RecalcFactionsDisasters('stop only')
        holder:UpdateFactionsDisasters()
        return holder.factions_disaster.A ~= nil, updates,
            messages[1], holder.factions_tension_warnings.A
    """)


def assert_deep_scan_route():
    root = Path(d.TREES["1.1.0"])
    tech = d.read(root / "Data/Tech.lua")
    stub = d.read(root / "Data/TechPreset.lua")
    classdef = d.read(root / "CommonLua/Libs/Research/ClassDefs/ClassDef-PresetDefs.generated.lua")
    tree = d.read(root / "Lua/TechTree.lua")
    exploration = d.read(root / "Lua/Exploration.lua")
    probe = d.read(root / "Lua/OrbitalProbe.lua")

    deep_marker = tech.index("Tech DeepScanning Description")
    deep_start = tech.rfind("PlaceObj('Tech', {", 0, deep_marker)
    deep_end = tech.index("\n\nPlaceObj('Tech', {", deep_start + 1)
    deep = tech[deep_start:deep_end]
    assert 'id = "DeepScanning"' in deep
    assert 'Label = "Consts"' in deep and 'Prop = "DeepScanAvailable"' in deep
    assert "PlaceObj('Effect_UnlockDeeperDeposits'" in deep
    assert 'GlobalMap = "Techs"' in classdef
    assert "preset:EffectsApply(UIColony)" in tree
    assert "return g_Consts.DeepScanAvailable ~= 0" in exploration
    assert 'UIColony:IsTechResearched("AdaptedProbes")' in probe

    stub_at = stub.index('id = "DeepScanning"')
    stub_body = stub[stub.rfind("PlaceObj('TechPreset', {", 0, stub_at):stub.index("})", stub_at) + 2]
    assert "Effect_ModifyLabel" not in stub_body
    return "live Tech carries both effects; TechPreset is an inert id/group stub; exploration reads DeepScanAvailable; probes separately require AdaptedProbes"


def completed_task(active):
    rt = d.lua_runtime()
    rt.execute("""
        Legislature = {}
        now = 1000
        function GameTime() return now end
        function ripairs(t)
            local i = #t + 1
            return function()
                i = i - 1
                if i > 0 then return i, t[i] end
            end
        end
    """)
    install(rt, "Lua/Factions/Legislature.lua", "Legislature:CheckActiveFactionTaskSuccess", "1.1.0")
    rt.globals().fixture_active = active
    return rt.execute("""
        local expired = {
            expiration_time = 900,
            RemoveEffect = function(self, idx)
                table.remove(holder.completed_faction_tasks, idx)
            end,
        }
        local active_task = fixture_active and {
            expiration_time = 2000,
            GetFactionTaskDef = function()
                return {EvalGenerateCondition = function() return true end}
            end,
            EvalSuccess = function() return false end,
            Dismiss = function() error('unexpected dismiss') end,
            Complete = function() error('unexpected complete') end,
        } or false
        holder = setmetatable({
            active_faction_task = active_task,
            completed_faction_tasks = {expired},
            active_faction_quests = {}, completed_faction_quests = {},
        }, {__index = Legislature})
        holder:CheckActiveFactionTaskSuccess()
        return #holder.completed_faction_tasks
    """)


def assert_first_session_popup_route():
    old_root = Path(d.TREES["1.0.7"])
    new_root = Path(d.TREES["1.1.0"])
    rel = Path("Lua/Factions/Legislature.lua")
    old = d.read(old_root / rel)
    new = d.read(new_root / rel)
    assert old.count("OpenFirstLegislatureSessionPopup") == 2
    assert new.count("OpenFirstLegislatureSessionPopup") == 1
    assert 'Msg("FirstLegislatureSessionPopupClosed")' in new
    preset = d.read(new_root / "Data/PopupNotifications/PopupNotificationPreset-Laws.lua")
    assert 'id = "EarthCouncilIntro"' in preset
    return "old declaration+BeginSession call became a new declaration only; the retained EarthCouncilIntro preset and new closure message have no literal consumer"


def main():
    print("PROGRESS SEAM DESK:", d.lua_version(), "(archived bodies; no runtime claim)")
    old = disaster("1.0.7", 0)
    zero = disaster("1.1.0", 0)
    one = disaster("1.1.0", 1)
    print("expired disaster 1.0.7:", old)
    print("expired disaster 1.1.0 zero seats:", zero)
    print("expired disaster 1.1.0 one seat:", one)
    assert old == (False, 0, "FactionDisasterStop", True), old
    assert zero == (True, 1, None, None), zero
    assert one == (False, 0, "FactionDisasterStop", True), one
    print("counterfactual one-seat branch stops and removes the disaster (control discriminates)")
    no_active = completed_task(False)
    with_active = completed_task(True)
    print("expired completed task, no active task:", no_active)
    print("expired completed task, active-task control:", with_active)
    assert no_active == 1, no_active
    assert with_active == 0, with_active
    print("counterfactual active-task branch removes the expired approval bonus (control discriminates)")
    print("First-session popup route:", assert_first_session_popup_route())
    print("DeepScanning route:", assert_deep_scan_route())
    print("PROBE SWEEP: clean")
    print("PASS: disaster and completed-task controls discriminate; popup orphan and research route are source-connected")


if __name__ == "__main__":
    main()
