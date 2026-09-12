#!/usr/bin/env python3
"""C90: missing Require targets through the REAL core and whole modules.

Desk evidence, never an engine/reachability claim. The k2 idea from
desk_c89_faction_gate is retained, but Require/Register/DataPatch/WhenActive
are not stubbed: their status transitions are part of the question.
Shipped trait data, label resolution, modifier bodies and Sinkhole classdef
are extracted verbatim. Preset construction/inheritance and messages are
fixtures; no class flattening, colony load or save healing is simulated.
The write proxies preserve first-pass values but not rawget after a write;
these are fresh-preset first-pass controls, not idempotency/reload tests.
"""
import re
from pathlib import Path
import deskbench as db


PRELUDE = db.ENGINE_SHIMS + r'''
LOGS = {}
ModLog = function(s) LOGS[#LOGS+1] = s end
-- The core's delayed menu dialog is irrelevant here; never execute its thread.
CreateRealTimeThread = function(fn) return {fn=fn} end
T = function(id, text) return text end
-- The module's probe supplies numeric scale=1; no engine point is constructed.
IsPoint = function(value)
  if type(value) ~= 'number' then error('unmodelled scale type') end
  return false
end
DataLoaded = true
-- Assignment must append handlers, as in the game, rather than overwrite them.
local handlers = {}
OnMsg = setmetatable({}, {__newindex = function(_, event, fn)
  handlers[event] = handlers[event] or {}
  table.insert(handlers[event], fn)
end})
function Msg(event, ...)
  for _, fn in ipairs(handlers[event]) do fn(...) end
end
WRITES = {}
function watch(name, data, class)
  return setmetatable({}, {
    __index = function(_, key)
      local value = data[key]
      if value ~= nil then return value end
      return class and class[key]
    end,
    __newindex = function(_, key, value)
      WRITES[#WRITES+1] = name .. '.' .. key .. '=' .. tostring(value)
      data[key] = value
    end,
    __pairs = function() return next, data, nil end,
  })
end
TraitPreset = {modify_trait='', modify_percent=0}
TraitPresets = {}
function PlaceObj(class, data)
  if class ~= 'TraitPreset' then error('unexpected preset class') end
  TraitPresets[data.id] = watch(data.id, data, TraitPreset)
end
LabelContainer = {}
DefineClass = {}
UndefineClass = function() end
'''


def shipped(rt, rel, pattern, tree='1.1.0'):
    text, start, _ = db.body(rel, pattern, tree)
    db.load_at(rt, text, '=' + rel, start)


def runtime():
    rt = db.lua_runtime()
    rt.execute(PRELUDE)
    db.load_at(rt, db.read(Path(db.REPO) / 'Code/00_Core.lua'), '=Code/00_Core.lua')
    return rt


def trait_data(rt, tree):
    rel = 'Data/TraitPreset.lua'
    text = db.read(Path(db.TREES[tree]) / rel)
    blocks = list(re.finditer(r"^PlaceObj\('TraitPreset', \{\n.*?^\}\)", text,
                              re.M | re.S))
    for name in ('Religious', 'Saint', 'Empath'):
        matches = [m for m in blocks if '\tid = "' + name + '",' in m.group()]
        assert len(matches) == 1, (tree, name)
        m = matches[0]
        db.load_at(rt, m.group(), '=' + rel, text[:m.start()].count('\n') + 1)
    rel = 'Lua/Traits.lua'
    text = db.read(Path(db.TREES[tree]) / rel)
    start = text.index('local fixed_labels = {')
    _, _, end_line = db.body(rel, r'^function GetTraitLabel\(', tree)
    first = text[:start].count('\n') + 1
    db.load_at(rt, '\n'.join(text.splitlines()[first-1:end_line]), '=' + rel, first)
    rel = ('Lua/TraitPreset.lua' if tree == '1.1.0'
           else 'Lua/ClassDefs/ClassDef-PresetDefs.generated.lua')
    shipped(rt, rel, r'^function TraitPreset:AddDomeColonistsModifier\(', tree)
    shipped(rt, 'CommonLua/PropertyObject.lua', r'^function GetPropScale\(', tree)
    shipped(rt, 'Lua/LabelContainer.lua', r'^function LabelContainer:SetLabelModifier\(', tree)


def load_module(rt, name):
    rel = 'Code/Fix_' + name + '.lua'
    db.load_at(rt, db.read(Path(db.REPO) / rel), '=' + rel)


def writes(rt):
    return list(rt.globals().WRITES.values())


def entry(rt, name):
    return rt.globals().SMRFixPack.fixes[name]


def saint(tree, missing=None, veto=False):
    rt = runtime()
    trait_data(rt, tree)
    if missing:
        rt.execute(missing + '=nil')
    if veto:
        rt.execute('SMRFixPack_Disabled.SaintBlessing=true')
    load_module(rt, 'SaintBlessing')
    before = entry(rt, 'SaintBlessing').status
    rt.execute('Msg("ClassesBuilt")')
    return rt, before


def sinkhole(missing=None, veto=False):
    rt = runtime()
    rel = 'Lua/BuildingTemplate/Sinkhole.generated.lua'
    db.load_at(rt, db.read(Path(db.TREES['1.1.0']) / rel), '=' + rel)
    shipped(rt, 'Lua/Buildings/Building.lua', r'^function DestroyBuildingImmediate\(')
    rt.execute('''
      Sinkhole=watch('class', DefineClass.Sinkhole)
      g_Classes={Sinkhole=Sinkhole}
      BuildingTemplates={Sinkhole=watch('template', {template_name='Sinkhole'}, Sinkhole)}
    ''')
    if missing == 'class':
        rt.execute('Sinkhole=nil; g_Classes.Sinkhole=nil')
    elif missing:
        rt.execute(missing + '=nil')
    if veto:
        rt.execute('SMRFixPack_Disabled.SinkholeIndestructible=true')
    load_module(rt, 'SinkholeIndestructible')
    before = entry(rt, 'SinkholeIndestructible').status
    rt.execute('Msg("ClassesBuilt")')
    return rt, before


def main():
    bench = db.Bench('C90 actual core: decline, ordered writes, and healing of status')
    for tree in ('1.0.7', '1.1.0'):
        expected = ['Saint.modify_trait=TraitReligious'] if tree == '1.0.7' else []
        for missing in (None, 'GetTraitLabel', 'TraitPreset.AddDomeColonistsModifier',
                        'LabelContainer.SetLabelModifier'):
            rt, before = saint(tree, missing)
            after = entry(rt, 'SaintBlessing').status
            stopped = missing in ('GetTraitLabel', 'TraitPreset.AddDomeColonistsModifier')
            branch_log = ('corrected 1 dome-colonists' if tree == '1.0.7'
                          else 'save re-base armed for 1 preset(s)')
            bench.check('%s Saint %s: exact writes and status' % (tree, missing or 'intact'),
                        before == ('inactive' if missing else 'active')
                        and after == ('inactive' if stopped else 'active')
                        and writes(rt) == ([] if stopped else expected)
                        and (stopped or any(branch_log in s for s in rt.globals().LOGS.values())),
                        '%s -> %s; %s' % (before, after, writes(rt)))
            if missing == 'LabelContainer.SetLabelModifier':
                bench.check('%s Saint failed self-check is erased from UpdateSuspects' % tree,
                            entry(rt, 'SaintBlessing').update_suspect is None
                            and len(rt.eval('SMRFixPack.UpdateSuspects()')) == 0)
                if tree == '1.1.0':
                    bench.check('1.1.0 Saint arms the save re-base despite decline',
                                any('save re-base armed for 1 preset(s)' in s
                                    for s in rt.globals().LOGS.values()))
        rt, before = saint(tree, veto=True)
        bench.check('%s Saint veto stops the pass' % tree,
                    before == 'disabled' and entry(rt, 'SaintBlessing').status == 'disabled'
                    and writes(rt) == [] and len(rt.globals().LOGS) == 1)

    expected = ['class.indestructible=true', 'template.indestructible=true']
    for missing in (None, 'class', 'DestroyBuildingImmediate'):
        rt, before = sinkhole(missing)
        after = entry(rt, 'SinkholeIndestructible').status
        bench.check('Sinkhole %s: exact ordered writes and status' % (missing or 'intact'),
                    before == ('inactive' if missing else 'active')
                    and after == ('inactive' if missing == 'class' else 'active')
                    and writes(rt) == ([] if missing == 'class' else expected),
                    '%s -> %s; %s' % (before, after, writes(rt)))
        if missing == 'DestroyBuildingImmediate':
            bench.check('Sinkhole failed self-check is erased from UpdateSuspects',
                        entry(rt, 'SinkholeIndestructible').update_suspect is None
                        and len(rt.eval('SMRFixPack.UpdateSuspects()')) == 0)
    rt, before = sinkhole(veto=True)
    bench.check('Sinkhole veto stops the pass',
                before == 'disabled' and entry(rt, 'SinkholeIndestructible').status == 'disabled'
                and writes(rt) == [])
    return bench.finish('ALL DEMANDS HELD -- injected target loss, not a field reproduction.')


if __name__ == '__main__':
    raise SystemExit(main())
