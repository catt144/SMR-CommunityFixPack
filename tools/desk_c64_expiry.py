#!/usr/bin/env python3
"""C64: completed-opportunity expiry stays inside active-task guard on build 25579348.

Extracts current CheckActiveFactionTaskSuccess and real FactionTask:RemoveEffect.
No active task and empty promise lists mean no refusing task methods are stubbed.
GameTime and ripairs are clock/iterator shims only. An in-memory falsifying
variant moves the identical completed-task cleanup outside the active-task
guard; it must reject retention. A not-yet-expired control stays retained.
No game, save, mod, document, or archive writes. Run from repo:
    python tools/desk_c64_expiry.py
"""
from pathlib import Path
import deskbench as d

ROOT = Path(__file__).resolve().parents[2] / "SMR-Shared/SMR-SrcArchive/1.1.1.406343/Src"
d.TREES["current"] = str(ROOT)


def run(variant, expired=True):
    rt = d.lua_runtime()
    rt.execute("""
        Legislature = {}; FactionTask = {}
        function GameTime() return 1000 end
        function ripairs(t)
            local i = #t + 1
            return function() i=i-1; if i>0 then return i,t[i] end end
        end
    """)
    text, first, last = d.body("Lua/Factions/Legislature.lua",
        "^function Legislature:CheckActiveFactionTaskSuccess[(]", "current")
    cleanup = "\t\tfor idx, task in ripairs(self.completed_faction_tasks) do\n\t\t\tif task.expiration_time <= GameTime() then\n\t\t\t\ttask:RemoveEffect(idx)\n\t\t\tend\n\t\tend"
    guarded = cleanup + "\n\tend"
    assert text.count(guarded) == 1, "shipped cleanup shape changed"
    if variant:
        text = text.replace(guarded, "\tend\n" + cleanup, 1)
    d.load_at(rt, text, "=Lua/Factions/Legislature.lua", first)
    remove, remove_first, remove_last = d.body("Lua/Factions/Legislature.lua",
        "^function FactionTask:RemoveEffect[(]", "current")
    d.load_at(rt, remove, "=Lua/Factions/Legislature.lua", remove_first)
    rt.globals().expiration = 900 if expired else 1100
    result = rt.execute("""
        local task = setmetatable({expiration_time=expiration}, {__index=FactionTask})
        g_Legislature = setmetatable({active_faction_task=false,
            completed_faction_tasks={task}, active_faction_quests={},
            completed_faction_quests={}}, {__index=Legislature})
        g_Legislature:CheckActiveFactionTaskSuccess()
        return #g_Legislature.completed_faction_tasks
    """)
    print(f"build=25579348 checker={first}-{last} RemoveEffect={remove_first}-{remove_last} variant={variant} expired={expired} retained={result}")
    return result


def main():
    shipped, falsifier, young = run(False), run(True), run(True, False)
    assert shipped == 1 and falsifier == 0 and young == 1
    print("PASS C64: expired retention predicate accepts shipped body and rejects unguarded-cleanup falsifier; young task survives")


if __name__ == "__main__":
    main()
