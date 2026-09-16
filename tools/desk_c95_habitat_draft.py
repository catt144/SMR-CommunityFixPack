#!/usr/bin/env python3
"""C95 desk falsifier. Extract current shipped bodies; never launch/provision a game.

Engine shims: nil-tolerant iteration, allocation, table.add/get/find, IsValid and
IsKindOf (ancestry parsed from shipped declarations). ObjModified is inert.
No pathing, transport, scheduling, UI or save serialization is measured here.
Synthetic fixtures state bucket membership explicitly; they are not a colony.
"""
import pathlib
import re
import subprocess

from deskbench import ENGINE_SHIMS, REPO, SRC_LIVE, body, load_at, span
from lupa.lua54 import LuaRuntime

ROOT = pathlib.Path(SRC_LIVE)
MODULE = pathlib.Path(REPO, 'Code/Fix_HabitatExpeditionDraft.lua')


def source_audit():
    parents, calls, loads = {}, [], []
    for p in ROOT.rglob('*.lua'):
        s = p.read_text(encoding='utf-8', errors='replace')
        for m in re.finditer(r'DefineClass\.(\w+)\s*=\s*\{\s*__parents\s*=\s*\{([^}]+)', s):
            parents[m[1]] = re.findall(r'"(\w+)"', m[2])
        for n, line in enumerate(s.splitlines(), 1):
            if 'FilterColonistsByTrait(' in line and not line.startswith('function '):
                calls.append(f'{p.relative_to(ROOT)}:{n}')
            if re.search(r'CargoTransporter\.Load\(|self:Load\(', line):
                loads.append((str(p.relative_to(ROOT)), n, line.strip()))
    direct = sorted(k for k, v in parents.items() if 'CargoTransporter' in v)
    descendants = {'CargoTransporter'}
    while True:
        more = descendants | {k for k, v in parents.items() if any(x in descendants for x in v)}
        if more == descendants:
            break
        descendants = more
    print('SOURCE filter calls (definition excluded):', len(calls), calls)
    print('SOURCE Load candidates:', len(loads), loads)
    print('SOURCE direct inheritors:', len(direct), direct)
    print('SOURCE transitive named DefineClass inheritors:', len(descendants)-1,
          sorted(descendants - {'CargoTransporter'}))
    assert len(calls) == 4
    assert direct == ['LanderRocketBase', 'RocketBase', 'RocketExpeditionBase']
    cargo_loads = [x for x in loads if 'CargoTransporter.Load(' in x[2]]
    assert len(cargo_loads) == 2 and {pathlib.Path(x[0]).name for x in cargo_loads} == {
        'LanderRocket.lua', 'RocketExpedition.lua'}
    assert all('MapDescriptor.lua' in x[0] for x in loads if x not in cargo_loads)
    return parents


def main():
    print('COMMAND: python tools/desk_c95_habitat_draft.py')
    print('HEAD:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
    acf = pathlib.Path(r'A:\SteamLibrary\steamapps\appmanifest_3215050.acf').read_text()
    print('BUILD:', re.search(r'"buildid"\s+"(\d+)"', acf)[1], 'lupa Lua 5.4')
    parents = source_audit()
    rt = LuaRuntime(unpack_returned_tuples=True)
    rt.execute(ENGINE_SHIMS)
    rt.execute('''
        ancestors = {}; CargoTransporter = {}; RocketExpeditionBase = {}
        LanderRocketBase = {}; CargoTransporterNew = {}; UniversalRocketBase = {}
        MicroGHabitatBase = {}; Colonist = {}
        g_RocketTypes = {Expedition='RocketExpedition'}
        local function derives(name, target)
            if name == target then return true end
            for _, parent in ipairs(ancestors[name]) do
                if derives(parent, target) then return true end
            end
            return false
        end
        function IsKindOf(obj, name) return type(obj) == 'table' and derives(obj.class, name) end
        function IsValid(obj) return type(obj) == 'table' and not obj.invalid end
        function ObjModified() end
        function createtable() return {} end
        table.add = function(t, item) t = t or {}; t[#t+1] = item; return t end
        table.find = function(t, item) for i,v in ipairs(t) do if v==item then return i end end end
        local native_error = error
        -- Retail error/assert report and CONTINUE, never use them as test assertions.
        loud = 0
        function error() loud = loud + 1 end
        function check(ok, msg) if not ok then native_error(msg, 2) end end
        SMRFixPack = {
            Register = function(id, spec) registered = spec end,
            Require = function(id, spec)
                for _, c in ipairs(spec) do
                    local val = c.class and _G[c.class] or c.global and _G[c.global]
                    if c.method then val = val and val[c.method] end
                    if c.path then val = table.get(_G, table.unpack(c.path)) end
                    local kind = c.kind or ((c.method or c.global) and 'function' or 'table')
                    if kind == 'any' and val == nil or kind ~= 'any' and type(val) ~= kind then
                        return 'missing dependency'
                    end
                end
            end,
        }
    ''')
    for cls, ps in parents.items():
        rt.globals().ancestors[cls] = rt.table_from(ps)
    # Each helper is extracted separately so the delimiter stays unambiguous.
    sources = []
    for name in ('copy', 'ifilter', 'union', 'subtraction'):
        sources.append(('CommonLua/Core/types.lua', '^function table.' + name + r'\('))
    sources.extend([
        ('CommonLua/Core/types.lua', r'^\s+function table.iappend\('),
        ('Lua/Buildings/Workplace.lua', '^function ValidateBuilding'),
        ('Lua/City.lua', '^function GetConnectedCities'),
        ('Lua/City.lua', '^function GetCityLabelWithConnected'),
        ('Lua/Units/Colonist.lua', '^function Colonist:IsDying'),
        ('Lua/Units/Colonist.lua', '^function Colonist:CanChangeCommand'),
        ('Lua/Units/Colonist.lua', '^function Colonist:IsTransported'),
        ('Lua/Buildings/CargoTransporter.lua', '^function GetConnectedCitiesForColonists'),
        ('Lua/Buildings/CargoTransporter.lua', '^function CargoTransporter:GatherAvailableColonists'),
        ('Lua/Buildings/RocketExpedition.lua', '^function RocketExpeditionBase:GatherAvailableColonists'),
        ('Lua/Buildings/LanderRocket.lua', '^function LanderRocketBase:GatherAvailableColonists'),
        ('Lua/CargoTransporterNew.lua', '^function CargoTransporterNew:GatherAvailableColonists'),
    ])
    for rel, pattern in sources:
        text, first, last = body(rel, pattern)
        # table.ifilter's insert is a file-local alias, not changed behavior.
        load_at(rt, 'local insert = table.insert\n' + text, '=' + rel, first-1)
        assert not re.search(r'\b(Sleep|WaitMsg|WaitWakeup|Create\w*Thread)\s*\(', text)
    rel = 'Lua/CargoTransporterNew.lua'
    text, first, last = span(rel, ['^local function build_unfavored_traits',
                                 '^function FilterColonistsByTrait',
                                 '^local function is_colonist_reachable'])
    load_at(rt, text, '=' + rel, first)
    assert not re.search(r'\b(Sleep|WaitMsg|WaitWakeup|Create\w*Thread)\s*\(', text)
    # Gather was compiled as its own extracted body, so expose its shipped file-local
    # callback as a harness global without rewriting the callback body.
    reach, first, last = body(rel, '^local function is_colonist_reachable')
    load_at(rt, reach.replace('local function ', 'function ', 1), '=' + rel, first)
    rt.execute('''
        function assert(ok) if not ok then loud = loud + 1 end return ok end
        empty_table = {}
        table.icopy = function(t)
            local out={}; for i=1,#t do out[i]=t[i] end; return out
        end
        function unit(id, home, command, workplace, traits)
            return {id=id, residence=home, command=command or 'Idle', workplace=workplace,
                traits=traits or {}, IsDead=function(self) return self.dead end,
                CanChangeCommand=function(self) return not self.blocked end}
        end
        nat = {class='NaturalistHabitat'}; micro = {class='MicroGHabitat'}
        dome = {class='Dome', allow_work_in_connected=false}
        home = {class='Residence', parent_dome=dome}
        job = {class='Workplace'}
        a=unit('naturalist',nat); b=unit('micro',micro)
        c=unit('idle',home); d=unit('busy',home,'Rest')
        e=unit('employed',home,'Idle',job); f=unit('busy employed',home,'Work',job)
        city={labels={Colonist={a,b,c,d,e,f},Elevator={}}}
        for _,u in ipairs(city.labels.Colonist) do u.city=city end
        rocket=setmetatable({class='RocketExpedition', city=city},{__index=RocketExpeditionBase})
        vanilla=CargoTransporter.GatherAvailableColonists; base_filter=FilterColonistsByTrait
        new_vanilla=CargoTransporterNew.GatherAvailableColonists
        universal=setmetatable({class='UniversalRocketBase', RocketType=g_RocketTypes.Expedition,
            city=city, cargo_request_passengers={}},{__index=CargoTransporterNew})
        function ids(list)
            local out={}; for _,u in ipairs(list) do out[#out+1]=u.id end
            return table.concat(out, ',')
        end
        check(ids(rocket:GatherAvailableColonists(4))=='naturalist,micro,idle,busy','vanilla control')
        check(ids(universal:GatherAvailableColonists(4))=='naturalist,micro,idle,busy','new vanilla control')
    ''')
    # Model the actual split environment: writes must reach the shipped global.
    rt.execute('''
        modenv=setmetatable({}, {__index=_G, __newindex=function(_,k,v) _G[k]=v end})
    ''')
    rt.eval('function(src) return load(src, "@Code/Fix_HabitatExpeditionDraft.lua", "t", modenv) end')(
        MODULE.read_text(encoding='utf-8'))()
    rt.execute('''
        check(registered.apply()==nil, 'apply')
        check(ids(rocket:GatherAvailableColonists(4))=='idle,busy,employed,busy employed','fill all buckets')
        check(ids(universal:GatherAvailableColonists(4))=='idle,busy,employed,busy employed','new fill all buckets')
        check(FilterColonistsByTrait==base_filter,'success restores exact global')
        check(#city.labels.Colonist==6 and city.labels.Colonist[1]==a,'pool never mutated')
        local lander=setmetatable({cargo_passengers={a,b}}, {__index=LanderRocketBase})
        check(ids(lander:GatherAvailableColonists(2))=='naturalist,micro','lander choice survives')
        local elevator=setmetatable({city=city,cargo_request_passengers={}}, {__index=CargoTransporterNew})
        check(ids(elevator:GatherAvailableColonists(2))=='naturalist,micro','elevator untouched')
        check(ids(CargoTransporter.GatherAvailableColonists({class='SupplyRocket',city=city},2))
            =='naturalist,micro','foreign receiver delegates')
        local homeless=unit('homeless',nil)
        city.labels.Colonist={homeless,c}
        check(ids(rocket:GatherAvailableColonists(2))=='homeless,idle','nil residence is normal')
        city.labels.Colonist={a,b,c,d,e,f}
        universal.cargo_request_passengers={a,b,c,d,e,f}
        local request_ids=ids(universal:GatherAvailableColonists(4))
        check(request_ids=='idle,busy,employed,busy employed',
            'new cargo request pool branch: '..request_ids)
        universal.cargo_request_passengers={}
        local real_kind=IsKindOf
        IsKindOf=function(obj, class)
            if class=='MicroGHabitatBase' then local absent=nil; return absent.fail end
            return real_kind(obj,class)
        end
        check(ids(rocket:GatherAvailableColonists(2))=='naturalist,micro','predicate error delegates')
        IsKindOf=real_kind
        -- Hard specialization, soft traits, transient destruction and connected-city input.
        c.traits={Scientist=true,Senior=true}; d.traits={Scientist=true}
        check(ids(rocket:GatherAvailableColonists(2,'Scientist'))=='idle,busy','specialization/soft fallback')
        d.thread_running_destructors=true
        check(ids(rocket:GatherAvailableColonists(2))=='idle,employed','transient pre-filter preserved')
        d.thread_running_destructors=nil; c.traits={}; d.traits={}
        city.labels.Colonist={a,b}; local other={labels={Colonist={c,d,e,f}}}
        for _,u in ipairs(other.labels.Colonist) do u.city=other end
        city.labels.Elevator={{other={city=other}}}
        check(ids(rocket:GatherAvailableColonists(4))=='idle,busy,employed,busy employed','connected city fill')
        check(ids(universal:GatherAvailableColonists(4))=='idle,busy,employed,busy employed',
            'new GetCityLabelWithConnected branch')
        city.labels.Elevator={}; city.labels.Colonist={a,b,c,d,e,f}
        for _,u in ipairs(city.labels.Colonist) do u.city=city end
        c.dead=true; d.blocked=true
        check(ids(universal:GatherAvailableColonists(2))=='employed,busy employed','new liveness filters')
        c.dead=nil; d.blocked=nil
        -- Force a genuine error in the called filter; the retry observes restoration.
        local calls=0
        local faulty=function(pool,...)
            calls=calls+1
            if calls==1 then local absent=nil; return absent.fail end
            return base_filter(pool,...)
        end
        FilterColonistsByTrait=faulty
        check(ids(rocket:GatherAvailableColonists(2))=='naturalist,micro','error fallback vanilla')
        check(FilterColonistsByTrait==faulty and calls==2,'error restoration and read-only retry')
        FilterColonistsByTrait=base_filter
        calls=0
        FilterColonistsByTrait=faulty
        check(ids(universal:GatherAvailableColonists(2))=='naturalist,micro','new error fallback vanilla')
        check(FilterColonistsByTrait==faulty and calls==2,'new error restoration and read-only retry')
        FilterColonistsByTrait=base_filter
        -- Falsifier: the rejected post-filter shape loses otherwise available crew.
        local bad=vanilla(rocket,4)
        for i=#bad,1,-1 do if bad[i]==a or bad[i]==b then table.remove(bad,i) end end
        check(#bad<4,'post-filter mutant must fail fill')
        check(#rocket:GatherAvailableColonists(4)==4,'actual fix fills same fixture')
        local new_bad=new_vanilla(universal,4)
        for i=#new_bad,1,-1 do if new_bad[i]==a or new_bad[i]==b then table.remove(new_bad,i) end end
        check(#new_bad<4,'new post-filter mutant must fail fill')
        check(#universal:GatherAvailableColonists(4)==4,'new fix fills same fixture')
        -- Calling the base directly isolates restoration from the known #nil caller defect.
        check(CargoTransporter.GatherAvailableColonists(rocket,20)==nil,'scarcity unchanged')
        check(CargoTransporterNew.GatherAvailableColonists(universal,20)==nil,'new scarcity unchanged')
        check(FilterColonistsByTrait==base_filter,'nil return restores')
        CargoTransporter.GatherAvailableColonists=vanilla
        CargoTransporterNew.GatherAvailableColonists=new_vanilla
        check(ids(rocket:GatherAvailableColonists(2))=='naturalist,micro','desk removal control')
        check(ids(universal:GatherAvailableColonists(2))=='naturalist,micro','new desk removal control')
        -- Preserve complete return tuples, including trailing nil, through pcall.
        CargoTransporter.GatherAvailableColonists=function() return nil, false, 'tail', nil end
        check(registered.apply()==nil,'tuple apply')
        local tuple=table.pack(CargoTransporter.GatherAvailableColonists(rocket))
        check(tuple.n==4 and tuple[1]==nil and tuple[2]==false and tuple[3]=='tail', 'tuple preservation')
        CargoTransporter.GatherAvailableColonists=vanilla
        CargoTransporterNew.GatherAvailableColonists=new_vanilla
        MicroGHabitatBase=nil
        check(registered.apply()=='missing dependency','Require declines absent class')
        check(CargoTransporter.GatherAvailableColonists==vanilla,'decline leaves original installed')
        MicroGHabitatBase={}
        CargoTransporter=nil; RocketExpeditionBase=nil
        check(registered.apply()==nil,'new-only receiver applies')
        check(ids(universal:GatherAvailableColonists(2))=='idle,busy','new-only receiver filters')
        CargoTransporter={GatherAvailableColonists=vanilla}; RocketExpeditionBase={}
        CargoTransporterNew=nil; UniversalRocketBase=nil
        check(registered.apply()==nil,'legacy-only receiver applies')
        check(ids(rocket:GatherAvailableColonists(2))=='idle,busy','legacy-only receiver filters')
        check(loud==0,'no loud error/assert calls')
    ''')
    print('PASS: both receiver contrasts; both habitats; full crew across buckets; lander; elevator; foreign receiver;')
    print('      New request/connected/liveness branches; nil residence; predicate error; traits; transient filter;')
    print('      exact restore/error fallback; post-filter mutants rejected; scarcity; desk removal; tuples;')
    print('      common/one-receiver Require behavior; no-yield source scan; silence.')
    print('LIMIT: no game boot, colony departure, UI, save removal or engine concurrency measured.')


if __name__ == '__main__':
    main()
