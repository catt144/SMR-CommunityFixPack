#!/usr/bin/env python3
"""C111 command-text control on shipped 1.1.1.405907 Colonist UI Lua.

Loads the shipped ColonistCommands table, Getui_command, destination getter and
selector from the archived source, then the whole production module. The fake
T/Untranslated values retain IDs and text; no retail renderer or save system is
run. --without-fix is the negative control and must fail the own-home assertion.
--module-revision REV loads that commit's module without changing the checkout.
The class defaults are extracted too: absent emigration_dome inherits false,
the live shape omitted by the original nil-only fixture. The old 7cf48a2 module
must miss that shape while still changing a synthetic nil-valued getter input.
"""
import argparse
import subprocess
from pathlib import Path

import deskbench as db
from luafn import read_lines


ROOT = Path(r"B:/Dev/SMR/SMR-Shared/SMR-SrcArchive/1.1.1.405907/Src")
REL = "Lua/Units/Colonist.lua"
MODULE = Path(db.REPO, "Code/Fix_RescueReturnText.lua")

PRELUDE = r'''
Colonist = {}
SMRFixPack = { result = false }
function SMRFixPack.Require(_, checks)
    for _, c in ipairs(checks) do
        local ok = false
        if c.class then
            ok = type(_G[c.class]) == "table" and type(_G[c.class][c.method]) == "function"
        elseif c.global then
            ok = type(_G[c.global]) == "function"
        elseif c.probe then
            local ran, verdict = pcall(c.probe)
            ok = ran and verdict == true
        end
        if not ok then return c.reason or "missing target" end
    end
end
function SMRFixPack.Register(id, spec)
    SMRFixPack.id = id
    SMRFixPack.result = spec.apply()
end
function T(id, text) return { id, text } end
function Untranslated(text) return { untranslated = text } end
function TGetID(t) return type(t) == "table" and type(t[1]) == "number" and t[1] or false end
function IsKindOf(obj, class) return type(obj) == "table" and obj.kind == class end
function IsValid(obj) return obj ~= nil and obj ~= false end
function IsKindOfClasses() return false end
function colonist(command, dome, destination, emigration, source, migration)
    return setmetatable({
        kind = "Colonist", command = command, dome = dome,
        transport_task = destination and {
            dest_dome = destination, source_dome = source or false,
            migration_dest = migration or false,
        } or false,
        emigration_dome = emigration,
        IsInWorkCommand = function() return false end,
    }, { __index = Colonist })
end
function dome(name)
    return { name = name, GetDisplayName = function(self) return self.name end,
        Select = function(self) self.selected = (self.selected or 0) + 1 end }
end
'''


def source_span(first, last):
    lines = read_lines(str(ROOT / REL))
    assert lines[first - 1].startswith("local ColonistCommands = {")
    assert lines[last - 1] == "end"
    text = "\n".join(lines[first - 1:last])
    assert 'Transport =  T(4333, "Moving to a new Dome:' in text
    return text


def check(label, condition):
    print(("PASS" if condition else "FAIL") + " " + label)
    return bool(condition)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--without-fix", action="store_true")
    ap.add_argument("--module-revision")
    args = ap.parse_args()
    module_text = (subprocess.check_output(
        ["git", "show", args.module_revision + ":Code/Fix_RescueReturnText.lua"],
        cwd=db.REPO, text=True, encoding="utf-8") if args.module_revision
        else db.read(str(MODULE)))
    print("MODULE " + ("absent" if args.without_fix else args.module_revision or "working-tree"))
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    # Both methods and their original hyperlink plumbing, with source offsets.
    lines = read_lines(str(ROOT / REL))
    defaults = "\n".join(line for line in lines[:150]
                         if line.strip().startswith(("emigration_dome =", "dreaming =")))
    assert defaults.count("emigration_dome = false,") == 1
    assert defaults.count("dreaming = false,") == 1
    rt.execute("for k, v in pairs({" + defaults + "}) do Colonist[k] = v end")
    db.load_at(rt, "\n".join(lines[4437 - 1:4440]), "=" + REL, 4437)
    db.load_at(rt, "\n".join(lines[4462 - 1:4465]), "=" + REL, 4462)
    db.load_at(rt, source_span(4629, 4716), "=" + REL, 4629)
    rt.execute('''
        HOME = dome("Brussels")
        OTHER = dome("Ares")
        RESCUE = colonist("Transport", HOME, HOME, nil)
        FALSE_RESCUE = colonist("Transport", HOME, HOME, false)
        HOME_RESCUE = colonist("Transport", HOME, HOME, HOME)
        NIL_RESCUE = colonist("Transport", HOME, HOME, nil)
        setmetatable(NIL_RESCUE, nil)
        DREAM = colonist("Transport", HOME, HOME, nil)
        DREAM.dreaming = true
        RELOCATE = colonist("Transport", HOME, OTHER, OTHER)
        WALK = colonist("TransportByFoot", OTHER, OTHER, OTHER)
        STALE = colonist("Transport", HOME, HOME, OTHER)
        SAME_DOME_ORDINARY = colonist("Transport", HOME, HOME, nil, HOME)
        JOURNEY_LEG = colonist("Transport", HOME, HOME, nil, nil, OTHER)
        VANILLA_RESCUE = RESCUE:Getui_command()
        VANILLA_RELOCATE = RELOCATE:Getui_command()
        VANILLA_DREAM = DREAM:Getui_command()
    ''')
    g = rt.globals()
    ok = check("shipped own-home command uses new-Dome ID 4333",
               g.VANILLA_RESCUE[1] == 4333)
    ok &= check("shipped class default resolves missing instance emigration_dome to false",
                rt.eval('rawget(RESCUE, "emigration_dome") == nil and RESCUE.emigration_dome == false'))
    ok &= check("shipped relocation names the destination",
                g.VANILLA_RELOCATE[1] == 4333 and
                "<EmigrationDomeDisplayName>" in g.VANILLA_RELOCATE[2])
    if not args.without_fix:
        db.load_at(rt, module_text, "=Code/Fix_RescueReturnText.lua")
        ok &= check("module applies against shipped command", g.SMRFixPack.result is None)

    rt.execute('''
        RESCUE_TEXT = RESCUE:Getui_command()
        FALSE_TEXT = FALSE_RESCUE:Getui_command()
        HOME_TEXT = HOME_RESCUE:Getui_command()
        NIL_TEXT = Colonist.Getui_command(NIL_RESCUE)
        DREAM_TEXT = DREAM:Getui_command()
        RELOCATE_TEXT = RELOCATE:Getui_command()
        WALK_TEXT = WALK:Getui_command()
        STALE_TEXT = STALE:Getui_command()
        ORDINARY_TEXT = SAME_DOME_ORDINARY:Getui_command()
        JOURNEY_TEXT = JOURNEY_LEG:Getui_command()
        LINK_NAME = RESCUE:GetEmigrationDomeDisplayName()
        RESCUE:SelectEmigrationDome()
        RELOCATE:SelectEmigrationDome()
    ''')
    print("OBS inherited_false_tid=" + str(g.RESCUE_TEXT[1])
          + " explicit_false_tid=" + str(g.FALSE_TEXT[1])
          + " synthetic_nil_returning=" + str(bool(g.NIL_TEXT.untranslated)))
    ok &= check("own-home ride says returning with native destination hyperlink",
                g.RESCUE_TEXT.untranslated ==
                "Returning to Dome: <h SelectEmigrationDome InfopanelSelect><em><EmigrationDomeDisplayName></em></h>")
    ok &= check("explicit false, synthetic nil and home-valued rescue all say returning",
                bool(g.FALSE_TEXT.untranslated) and bool(g.NIL_TEXT.untranslated)
                and bool(g.HOME_TEXT.untranslated))
    ok &= check("dreaming keeps the native non-4333 result",
                rt.eval('DREAM_TEXT == VANILLA_DREAM and TGetID(DREAM_TEXT) ~= 4333'))
    ok &= check("own-home hyperlink names and selects home",
                g.LINK_NAME == "Brussels" and g.HOME.selected == 1)
    ok &= check("real relocation retains its destination text and link",
                g.RELOCATE_TEXT[1] == 4333 and g.OTHER.selected == 1)
    ok &= check("walk, stale emigration and non-rescue tasks remain native",
                g.WALK_TEXT[1] == 4333 and g.STALE_TEXT[1] == 4333
                and g.ORDINARY_TEXT[1] == 4333 and g.JOURNEY_TEXT[1] == 4333)

    # A new Lua runtime models a load/reload: no process-local origin marker.
    if not args.without_fix:
        fresh = db.lua_runtime()
        fresh.execute(PRELUDE)
        fresh.execute("for k, v in pairs({" + defaults + "}) do Colonist[k] = v end")
        db.load_at(fresh, "\n".join(lines[4437 - 1:4440]), "=" + REL, 4437)
        db.load_at(fresh, "\n".join(lines[4462 - 1:4465]), "=" + REL, 4462)
        db.load_at(fresh, source_span(4629, 4716), "=" + REL, 4629)
        db.load_at(fresh, module_text, "=Code/Fix_RescueReturnText.lua")
        fresh.execute('''
            HOME = dome("Brussels")
            RESCUE = colonist("Transport", HOME, HOME, nil)
            RELOADED_TEXT = RESCUE:Getui_command()
        ''')
        ok &= check("reloaded live task still shows returning",
                    bool(fresh.globals().RELOADED_TEXT.untranslated) and
                    fresh.globals().RELOADED_TEXT.untranslated == g.RESCUE_TEXT.untranslated)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
