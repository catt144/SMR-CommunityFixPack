#!/usr/bin/env python3
"""C96 desk falsifier. Extract current shipped bodies; never launch/provision a game.

Runs the SHIPPED ListAvailableRovers / GatherAvailableRovers / AddCargoAmount
bodies from both transporter implementations against synthetic rover fixtures,
before and after the module applies. Every harm leg is based on the PRE-FIX body.

Engine shims: nil-tolerant iteration, table.ifilter/insert, IsKindOf and
ClassDescendantsList over ancestry parsed from the shipped declarations.
No pathing, UI, save serialization or real colony is measured here; fixtures
state label membership and idleness explicitly, and are not a colony.
"""
import pathlib
import re
import subprocess

from deskbench import ENGINE_SHIMS, REPO, SRC_LIVE, body, load_at
from lupa.lua54 import LuaRuntime

ROOT = pathlib.Path(SRC_LIVE)
MODULE = pathlib.Path(REPO, 'Code/Fix_RoverSubclassManifest.lua')

# The two gates this fix exists for, one per implementation.
GATES = [
    ('Lua/Buildings/CargoTransporter.lua', 'CargoTransporter',
     'self.city.labels[class] or empty_table'),
    ('Lua/CargoTransporterNew.lua', 'CargoTransporterNew',
     'GetCityLabelWithConnected(self.city, class)'),
]


def source_audit():
    """The premise: BOTH implementations carry BOTH gates, and rovers register leaf-only."""
    parents = {}
    for p in ROOT.rglob('*.lua'):
        s = p.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'DefineClass\.(\w+)\s*=\s*\{\s*__parents\s*=\s*\{([^}]+)', s):
            parents[m[1]] = re.findall(r'"(\w+)"', m[2])

    for rel, cls, source_gate in GATES:
        text, first, _ = body(rel, r'^function %s:ListAvailableRovers\(' % cls)
        assert 'unit.class == class' in text, (rel, 'leaf compare gone')
        assert source_gate in text, (rel, 'source-list gate changed')
        print('SOURCE %-22s ListAvailableRovers:%-4d leaf-compare + leaf-label source list PRESENT'
              % (cls, first))

    reg = body('Lua/Buildings/BaseRover.lua', r'^function BaseRover:AddToCityLabels\(')[0]
    assert 'AddToLabel(self.class, self)' in reg
    assert '__parents' not in reg, 'registration now walks the parent chain — the gate may be gone'
    # It also registers "Unit" and "Rover"; only the class-named label gates the lister.
    assert 'AddToLabel("Rover", self)' in reg
    print('SOURCE BaseRover:AddToCityLabels registers Unit + Rover + the LEAF class, and '
          'nothing walks __parents — the source-list gate')

    # Directional relationships this repairs, and the one it must NOT.
    assert 'RCRover' in parents.get('RCSensor', []), 'RCSensor is no longer an RCRover'
    assert 'RCRover' in parents.get('RCSolar', []), 'RCSolar is no longer an RCRover'
    assert 'RCRover' not in parents.get('AttackRover', []), 'AttackRover became an RCRover'
    print('SOURCE RCSensor + RCSolar derive RCRover; AttackRover does NOT (hostile-rover leg)')
    return parents


FIXTURE = '''
    ancestors = {}
    empty_table = {}
    CargoTransporter = {}; CargoTransporterNew = {}
    BaseRover = {}; RCRover = {}; RCSensor = {}; RCSolar = {}
    AttackRover = {}; RCTransport = {}; Drone = {}

    local function derives(name, target)
        if name == target then return true end
        for _, parent in ipairs(ancestors[name] or empty_table) do
            if derives(parent, target) then return true end
        end
        return false
    end
    function IsKindOf(obj, name)
        if type(obj) ~= 'table' then return false end
        return derives(obj.class or obj.__name, name)
    end
    function ClassDescendantsList(anc)
        local out = {}
        for name in pairs(g_Classes) do
            if name ~= anc and derives(name, anc) then out[#out+1] = name end
        end
        table.sort(out)
        return out
    end
    function IsValid(obj) return type(obj) == 'table' and not obj.invalid end
    function ObjModified() end
    table.ifilter = function(t, f)
        local out = {}
        for i, v in ipairs(t or empty_table) do if f(v, i) then out[#out+1] = v end end
        return out
    end
    table.sortby_field = function(t, field)
        table.sort(t, function(a, b) return a[field] < b[field] end)
    end
    function GetCityLabelWithConnected(city, label) return city.labels[label] or empty_table end

    loud = 0
    local native_error = error
    function error() loud = loud + 1 end
    function check(ok, msg) if not ok then native_error(msg, 2) end end

    SMRFixPack = {
        Register = function(id, spec) registered = spec end,
        Require = function(id, spec)
            for _, c in ipairs(spec) do
                local val = c.class and _G[c.class] or c.global and _G[c.global]
                if c.method then val = val and val[c.method] end
                local kind = c.kind or ((c.method or c.global) and 'function' or 'table')
                if type(val) ~= kind then return 'missing dependency: ' .. tostring(c.class or c.global) end
            end
        end,
    }

    -- A transporter that is far from everything at a fixed point.
    function MakeTransporter(cls, labels, cargo)
        local t = setmetatable({ class = cls, city = { labels = labels }, cargo = cargo,
                                 x = 0 }, { __index = _G[cls] })
        return t
    end
    function MakeRover(cls, dist, opts)
        opts = opts or {}
        return { class = cls, drones = {}, x = dist,
                 idle = opts.idle ~= false, controllable = opts.controllable ~= false,
                 holder = opts.holder }
    end
'''

# Shipped methods need these instance helpers; they are behaviour we do not model.
METHODS = '''
    local function common(T)
        T.GetDist2D = function(self, u) return u.x - self.x end
        T.GetAvailableDronesFilter = function() return true end
        T.CanBeControlled = nil
    end
    common(CargoTransporter); common(CargoTransporterNew)
    local function rover_methods(r) end
    -- rover-side predicates the shipped filter calls
    getmetatable_rover = nil
'''


def build_runtime(parents, apply_module):
    rt = LuaRuntime(unpack_returned_tuples=True)
    rt.execute(ENGINE_SHIMS)
    rt.execute(FIXTURE)
    for cls, ps in parents.items():
        rt.globals().ancestors[cls] = rt.table_from(ps)
    # g_Classes holds only the classes these legs name; ClassDescendantsList walks it.
    rt.execute('''
        g_Classes = { BaseRover = BaseRover, RCRover = RCRover, RCSensor = RCSensor,
                      RCSolar = RCSolar, AttackRover = AttackRover, RCTransport = RCTransport,
                      CargoTransporter = CargoTransporter, CargoTransporterNew = CargoTransporterNew }
        for name, def in pairs(g_Classes) do def.__name = name end
        -- __ancestors, as the engine exposes it, for the cargo-credit remap
        for name, def in pairs(g_Classes) do
            local anc = {}
            local function walk(n)
                for _, p in ipairs(ancestors[n] or empty_table) do anc[p] = true; walk(p) end
            end
            walk(name)
            def.__ancestors = anc
        end
        -- rover instances answer the shipped filter's predicates
        RoverMT = { __index = { CanBeControlled = function(self) return self.controllable end,
                                IsIdle = function(self) return self.idle end } }
    ''')
    rt.execute(METHODS)

    for rel, cls, _ in GATES:
        for sel in ('ListAvailableRovers', 'GatherAvailableRovers'):
            text, first, _ = body(rel, r'^function %s:%s\(' % (cls, sel))
            assert not re.search(r'\b(Sleep|WaitMsg|WaitWakeup|Create\w*Thread)\s*\(', text), \
                '%s:%s can yield — the widen flag would be observable' % (cls, sel)
            load_at(rt, text, '=' + rel, first - 1)
    text, first, _ = body('Lua/CargoTransporterNew.lua', r'^function CargoTransporterNew:AddCargoAmount\(')
    load_at(rt, text, '=Lua/CargoTransporterNew.lua', first - 1)
    rt.execute('''
        function CargoTransporterNew:GetCargoAmount(id)
            return (self.cargo[id] and self.cargo[id].amount) or 0
        end
        function CargoTransporterNew:SetCargoAmount(id, v) self.cargo[id].amount = v end
    ''')

    if apply_module:
        rt.execute(MODULE.read_text(encoding='utf-8'))
        rt.execute('registered.apply()')
    return rt


def gather(rt, cls, want, amount, rovers):
    """Run the shipped gather for `want` over a label table built from `rovers`."""
    rt.globals().FIXTURE_ROVERS = rt.table_from([])
    rt.execute('labels = {}')
    for r_cls, dist in rovers:
        rt.execute('''
            labels['%s'] = labels['%s'] or {}
            local r = MakeRover('%s', %d)
            setmetatable(r, RoverMT)
            labels['%s'][#labels['%s'] + 1] = r
        ''' % (r_cls, r_cls, r_cls, dist, r_cls, r_cls))
    rt.execute("T = MakeTransporter('%s', labels, {})" % cls)
    out = rt.eval("T:GatherAvailableRovers('%s', %d)" % (want, amount))
    return [out[i]['class'] for i in range(1, len(out) + 1)] if out else []


def main():
    print('COMMAND: python tools/desk_c96_rover_subclass.py')
    print('HEAD:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
    acf = pathlib.Path(r'A:\SteamLibrary\steamapps\appmanifest_3215050.acf').read_text()
    print('BUILD:', re.search(r'"buildid"\s+"(\d+)"', acf)[1], 'lupa Lua 5.4')

    parents = source_audit()
    pre = build_runtime(parents, apply_module=False)
    post = build_runtime(parents, apply_module=True)

    results = []

    def leg(name, ok):
        results.append(name)
        assert ok, 'LEG FAILED: ' + name

    for cls in ('CargoTransporter', 'CargoTransporterNew'):
        seeker_only = [('RCSensor', 10)]
        # 1. the defect, on the PRE-FIX body
        leg('%s vanilla refuses a Seeker for an RCRover request' % cls,
            gather(pre, cls, 'RCRover', 1, seeker_only) == [])
        # 2. the repair
        leg('%s fixed accepts the Seeker' % cls,
            gather(post, cls, 'RCRover', 1, seeker_only) == ['RCSensor'])
        # 3. no behaviour change when vanilla can already satisfy it
        both = [('RCRover', 50), ('RCSensor', 10)]
        leg('%s satisfiable request keeps vanilla pick (nearest RCRover, NOT the nearer Seeker)' % cls,
            gather(pre, cls, 'RCRover', 1, both) == gather(post, cls, 'RCRover', 1, both) == ['RCRover'])
        # 4. directional: a base never satisfies a request for its subclass
        leg('%s base does NOT satisfy a Seeker request' % cls,
            gather(post, cls, 'RCSensor', 1, [('RCRover', 10)]) == [])
        # 5. the hostile-rover leg
        leg('%s AttackRover is never offered for an RCRover request' % cls,
            gather(post, cls, 'RCRover', 1, [('AttackRover', 5)]) == [])
        # 6. it repairs more than the Seeker
        leg('%s RCSolar also satisfies an RCRover request' % cls,
            gather(post, cls, 'RCRover', 1, [('RCSolar', 7)]) == ['RCSolar'])
        # 7. shortfall stays a shortfall when nothing can fill it
        leg('%s unfillable request still returns empty' % cls,
            gather(post, cls, 'RCRover', 2, seeker_only) == [])
        # 8. mixed fill uses both, nearest first
        mixed = [('RCRover', 40), ('RCSensor', 5)]
        leg('%s a 2-rover request fills from both, nearest first' % cls,
            gather(post, cls, 'RCRover', 2, mixed) == ['RCSensor', 'RCRover'])
        # 9. non-rover requests are untouched
        leg('%s a non-rover class is not widened' % cls,
            gather(pre, cls, 'Drone', 1, []) == gather(post, cls, 'Drone', 1, []) == [])

    # 10-12. the cargo line must be credited to the REQUESTED class
    def credit(rt, cargo, loaded):
        rt.execute("T = MakeTransporter('CargoTransporterNew', {}, %s)" % cargo)
        rt.execute("T:AddCargoAmount('%s', 1)" % loaded)
        return {k: rt.eval("T.cargo['%s'].amount" % k)
                for k in re.findall(r"(\w+)\s*=\s*\{", cargo)}

    leg('vanilla credits NOTHING when a Seeker is loaded against an RCRover line',
        credit(pre, "{ RCRover = { amount = 0, requested = 1 } }", 'RCSensor') == {'RCRover': 0})
    leg('fixed credits the RCRover line when a Seeker is loaded against it',
        credit(post, "{ RCRover = { amount = 0, requested = 1 } }", 'RCSensor') == {'RCRover': 1})
    leg('fixed still credits the exact line when one exists',
        credit(post, "{ RCSensor = { amount = 0, requested = 1 }, RCRover = { amount = 0, requested = 1 } }",
               'RCSensor') == {'RCSensor': 1, 'RCRover': 0})

    # 13. nothing threw anywhere
    leg('no shipped error() path was taken in any leg',
        pre.globals().loud == 0 and post.globals().loud == 0)

    print('PASS: ' + '; '.join(results))
    print('LIMIT: no game boot, real colony, pathing, UI, launch readiness or save '
          'serialization measured. Label membership and idleness are stated by the fixture.')


if __name__ == '__main__':
    main()
