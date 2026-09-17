#!/usr/bin/env python3
"""Registered C95 return repair, extracted shipped selector/dispatcher controls.

Synthetic route answers do not measure pathfinding. CommandObject.SetCommand
records dispatch instead of starting engine threads. Housing/trait/life-support
predicates are explicit fixture inputs, with rejection legs. No serialization,
colony creation, animation or travel timing is simulated.
"""
from pathlib import Path
import hashlib
import re
import subprocess

from deskbench import ENGINE_SHIMS, REPO, body, load_at, Bench, lua_runtime

MODULE = Path(REPO, 'Code/Fix_HabitatExpeditionReturn.lua')
ARRIVAL = Path(REPO, 'Code/Fix_ArrivalDeaths.lua')
SOURCES = [
    ('Lua/_GameUtils.lua', 'ChooseDome'),
    ('Lua/Units/Colonist.lua', 'Colonist:GetExpeditionReturnDome'),
    ('Lua/Units/Colonist.lua', 'Colonist:UpdateResidence'),
    ('Lua/Units/ColonistTransport.lua', 'Colonist:SetCommand'),
    ('Lua/Units/ColonistTransport.lua', 'Colonist:ReturnFromExpedition_TransportDestination'),
    ('Lua/Units/ColonistTransport.lua', 'Colonist:StartTransport'),
    ('Lua/Buildings/Residence.lua', 'Residence:ReserveResidence'),
    ('Lua/Buildings/Residence.lua', 'Residence:CanReserveResidence'),
    ('Lua/Buildings/Residence.lua', 'Residence:CancelResidenceReservation'),
    ('Lua/Units/Colonist.lua', 'Colonist:CancelResidenceReservation'),
    ('Lua/CargoTransporterNew.lua', 'CargoTransporterNew:UnloadPassengers'),
    ('Lua/Buildings/RocketBase.lua', 'RocketBase:Disembark'),
    ('Lua/Buildings/Community.lua', 'Community:CanVisit'),
    ('Lua/Buildings/MicroGHabitat.lua', 'MicroGHabitatBase:CanVisit'),
]


def runtime():
    rt = lua_runtime(unpack_returned_tuples=True)
    rt.execute(ENGINE_SHIMS)
    rt.execute('''
    Colonist={}; Residence={}; CommandObject={}; TransportTicket={}
    CargoTransporterNew={}; RocketBase={}; Community={}; MicroGHabitatBase={}
    function IsValid(x) return type(x)=='table' and not x.invalid end
    function IsKindOf(x,k) return IsValid(x) and x.kind==k end
    function IsSameMap(a,b) return a.map==b.map end
    function IsInWalkingDist(home,origin,city) return origin.walk end
    function GetTransportRoute(origin,home,check_use,allow_reachable)
      assert(check_use==true and allow_reachable==false)
      if origin.train and origin.map==home.map then return {station=1},{station=2} end
    end
    function GameTime() return 100 end
    function Sleep() end
    SessionRandom={Random=function() return 0 end}
    function GetSortedColonistSpecializationTable() return {} end
    function ripairs(t)
      local i=#t+1; return function() i=i-1; if i>0 then return i,t[i] end end
    end
    function Colonist:Idle() end
    function Colonist:OnArrival() end
    function Colonist:Arrive() end
    function Community:HasLifeSupport() return true end
    function Community:CanAcceptNewColonists() return true end
    function Community:GetScoreFor() return 0 end
    function Residence:IsSuitable() return true end
    function ValidateBuilding(x) return x end
    const={Scale={Stat=1000}}; g_CObjectFuncs={GetMapSlot=function() return 1 end}
    SMRFixPack={defs={},logs=0,Register=function(id,spec) SMRFixPack.defs[id]=spec end,
      Log=function() SMRFixPack.logs=SMRFixPack.logs+1 end,
      Require=function(id,spec)
        for _,c in ipairs(spec) do
          local v=c.class and _G[c.class] or c.global and _G[c.global]
          if c.method then v=v and v[c.method] end
          if c.path then v=table.get(_G,table.unpack(c.path)) end
          local k=c.kind or ((c.method or c.global) and 'function' or 'table')
          if type(v)~=k then return 'missing dependency' end
        end
      end}
    function Colonist:Appear(rocket) self.appear_location=rocket end
    function CargoTransporterNew:ResetPassengerCargoAmounts() end
    function GetDomesReachableByColonists() return test_domes,test_safety,test_dist or {},{} end
    g_Consts={CommunityEvalNone=-1000}
    table.find=function(t,v) for i,x in ipairs(t) do if x==v then return i end end end
    function CommandObject.SetCommand(self,cmd,a,b)
      self.issued={cmd,a,b}; return 'issued',nil,'tail'
    end
    function TransportTicket:new(t) return t end
    function Colonist:HasMember(k) return self[k]~=nil end
    function Colonist:HasLocalAccess(d) return self.holder.walk end
    function Colonist:GetTransportRoute(d,cmd)
      return GetTransportRoute(self.holder,d,true,false)
    end
    function Colonist:DiscardTransportTicket() self.transport_ticket=false end
    function Colonist:UpdateWorkplace()
      self.work_calls=(self.work_calls or 0)+1
      self.hired_in_dome=not IsKindOf(self.residence,'MicroGHabitatBase')
      return 'work',nil,'tail'
    end
    function Colonist:CanChangeCommand() return not self.blocked end
    function Colonist:CheckForcedResidence() return self.forced end
    function Colonist:SetResidence(h) self.residence=h end
    function home()
      return setmetatable({kind='MicroGHabitatBase', map=1, ui_working=true,
        accept_colonists=true, support=true, visit=true, suitable=true,
        GetScoreFor=function() return 100 end,
        HasFreeLivingSpaceFor=function(s) return s.free>0 end,
        CanAcceptNewColonists=function(s) return s.accept_colonists and s.ui_working end,
        reserved={}, free=0, colonists={},
        HasLifeSupport=function(s) return s.support end,
        CanVisit=function(s,u) return s.visit end,
        IsSuitable=function(s,u) return s.suitable end,
        GetFreeSpace=function(s) return s.free end,

        ChooseResidence=function(s,u) return s.suitable and s or false end,
      },{__index=Residence})
    end
    function subject(walk,train)
      local h=home()
      local u=setmetatable({traits={},city={},holder={walk=walk,train=train,map=1,
        IsValidPos=function() return true end,
        GetPos=function(s) return s end},expedition_residence=h,
        reserved_residence=h}, {__index=Colonist})
      h.reserved[1]=u; h.reserved[u]=true
      return u,h
    end
    ''')
    for rel, selector in SOURCES:
        code, first, _ = body(rel, '^function ' + re.escape(selector) + r'\(')
        load_at(rt, code, '=' + rel, first)
    return rt


def main():
    print('COMMAND: python tools/desk_c95_return_home.py')
    print('HEAD:', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
    acf = Path(r'A:/SteamLibrary/steamapps/appmanifest_3215050.acf').read_text()
    print('BUILD Steam:', re.search(r'"buildid"\s+"(\d+)"', acf)[1])
    print('MODULE sha256:', hashlib.sha256(MODULE.read_bytes()).hexdigest())
    for rel, selector in SOURCES:
        text, first, last = body(rel, '^function ' + re.escape(selector) + r'\(')
        canonical = '\n'.join(line.rstrip() for line in text.splitlines())
        print('SOURCE', rel, selector, f'lines={first}-{last} count={last-first+1}',
              'sha256=' + hashlib.sha256(canonical.encode()).hexdigest())
    b = Bench('C95/C102 registered return repair (desk only)')
    rt = runtime()
    rt.execute('u,h=subject(false,true); original=Colonist.GetExpeditionReturnDome')
    b.check('vanilla loses absent rail habitat', rt.eval('u:GetExpeditionReturnDome({}) == nil'))
    rt.execute("Colonist.SetCommand(u,'ReturnFromExpedition',u.holder,h)")
    b.check('vanilla dispatcher already books arrival train', rt.eval(
        "u.issued[1]=='DisembarkOnArrival' and u.transport_ticket.reason=='MigrateByTrain'"
        " and u.transport_ticket.destination==h and u.transport_ticket.param==false"))
    rt.execute('u,h=subject(false,false); wrong=home(); wrong.free=1; wrong:ReserveResidence(u)')
    b.check('fallback reservation erases expedition home before return', rt.eval(
        'u.reserved_residence==wrong and u.expedition_residence==false and not h.reserved[u]'))
    rt.execute(MODULE.read_text(encoding='utf-8'))
    rt.execute("assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil)")
    cases = [('walk', True, False, True), ('rail', False, True, True),
             ('disconnected', False, False, False)]
    for label, walk, train, expect in cases:
        rt.execute(f'u,h=subject({str(walk).lower()},{str(train).lower()}); candidates={{}}; chosen=u:GetExpeditionReturnDome(candidates)')
        b.check(label + ' route admission', rt.eval('chosen==h') == expect)
        b.check(label + ' shared input not mutated', rt.eval('#candidates==0'))
    for label, setup in [
        ('destroyed', 'h.invalid=true'), ('closed', 'h.ui_working=false'),
        ('refuses arrivals', 'h.accept_colonists=false'), ('no life support', 'h.support=false'),
        ('cannot visit', 'h.visit=false'), ('unsuitable home', 'h.suitable=false'),
        ('reservation lost', 'u.reserved_residence=false'), ('different map', 'h.map=2'),
    ]:
        rt.execute('u,h=subject(false,true); ' + setup)
        b.check(label + ' delegates without admitting home', rt.eval('u:GetExpeditionReturnDome({})==nil'))
    rt.execute('u,h=subject(true,false); h.kind="Dome"; candidates={h}')
    b.check('ordinary dome return preserved', rt.eval('u:GetExpeditionReturnDome(candidates)==h'))
    rt.execute('u,h=subject(true,false); candidates={h}')
    b.check('already reachable home preserved', rt.eval('u:GetExpeditionReturnDome(candidates)==h and #candidates==1'))
    rt.execute('u,h=subject(false,true); chosen=u:GetExpeditionReturnDome({}); chosen:ReserveResidence(u); u:SetCommand("ReturnFromExpedition",u.holder,chosen)')
    b.check('selected rail home retains original bed and native ticket', rt.eval(
        'u.reserved_residence==h and h.reserved[u] and u.transport_ticket.destination==h'))
    for receiver in ['new', 'legacy']:
        rt.execute('''u,h=subject(false,true); test_domes={}; test_safety=false
        rocket=u.holder; rocket.city=u.city; rocket.transported_passengers={u}
        rocket.cargo={any_specialization={amount=1}}
        setmetatable(rocket,{__index=CargoTransporterNew})''')
        rt.execute('rocket:UnloadPassengers()' if receiver == 'new' else 'RocketBase.Disembark(rocket,{u})')
        b.check(receiver + ' receiver returns all-habitat subject to held home', rt.eval(
            'u.transport_ticket.destination==h and h.reserved[u] and u.issued[1]=="DisembarkOnArrival"'))
    rt.execute('u,h=subject(true,false); h.free_spaces={inclusive=0}; h.CanVisit=MicroGHabitatBase.CanVisit')
    b.check('shipped full-habitat gate rejects anonymous visitor', rt.eval('not h:CanVisit()'))
    b.check('shipped full-habitat gate accepts its reserved returnee', rt.eval('h:CanVisit(u)'))
    b.check('module also restores full nearby habitat omitted by CanVisit', rt.eval('u:GetExpeditionReturnDome({})==h'))
    rt.execute('u,h=subject(true,false); u.dome=h; result=table.pack(u:UpdateWorkplace())')
    b.check('housing precedes picker at rejoin', rt.eval('u.residence==h and not u.hired_in_dome and u.work_calls==1'))
    b.check('work wrapper preserves nil-bearing return tuple', rt.eval('result.n==3 and result[1]=="work" and result[2]==nil and result[3]=="tail"'))
    rt.execute('u,h=subject(true,false); u.dome={}; u:UpdateWorkplace()')
    b.check('foreign dome does not get reassigned', rt.eval('u.residence==nil and u.work_calls==1'))
    rt.execute('u,h=subject(true,false); u.dome=h; u.blocked=true; u:UpdateWorkplace()')
    b.check('housing allocator refusal is respected (known gap)', rt.eval('u.residence==nil and u.work_calls==1'))
    # The installed recipe only stores class/global functions, with no runtime fields.
    b.check('module adds no persisted state or yielding body', not re.search(
        r'\b(?:GameVar|CreateGameTimeThread|Sleep|WaitMsg|SetResidence)\s*\(',
        '\n'.join(line for line in MODULE.read_text().splitlines() if not line.lstrip().startswith('--'))))
    for shape in ['nil', '{kind="Dome"}', '{kind="Residence"}', '{kind="Other"}']:
        delegated=runtime()
        delegated.execute("calls=0; function Colonist:GetExpeditionReturnDome(d,...) calls=calls+1; seen=d; return false,nil,'tail',... end")
        delegated.execute(MODULE.read_text(encoding='utf-8'))
        delegated.execute('assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil); u,h=subject(true,false); u.expedition_residence='+shape+"; candidates={}; result=table.pack(u:GetExpeditionReturnDome(candidates,42,nil))")
        b.check('non-habitat '+shape+' delegates exact arguments and returns', delegated.eval("calls==1 and seen==candidates and result.n==5 and result[1]==false and result[3]=='tail' and result[4]==42"))
    rt.execute('u,h=subject(true,false); u.residence=h; u.reserved_residence=false; h.reserved={}; h.colonists={u}')
    b.check('shipped reservation predicate refuses second slot in occupied full habitat', rt.eval('not h:CanReserveResidence(u)'))
    b.check('draft admits its existing suitable bed before reservation', rt.eval('SMRFixPack.HabitatExpeditionReturn.CanReturnHome(u,h,u.holder)'))
    rt.execute('h.suitable=false')
    b.check('occupied but unsuitable home still excluded', rt.eval('not SMRFixPack.HabitatExpeditionReturn.CanReturnHome(u,h,u.holder)'))
    rt.execute('h.suitable=true; u.holder.walk=false')
    b.check('occupied full habitat without return route excluded', rt.eval('not SMRFixPack.HabitatExpeditionReturn.CanReturnHome(u,h,u.holder)'))
    rt.execute("before=Colonist.GetExpeditionReturnDome; SMRFixPack.defs.HabitatExpeditionReturn.apply()")
    b.check('return apply idempotent', rt.eval('before==Colonist.GetExpeditionReturnDome'))
    # Save the pre-C102 selector as the harm control; do not base it on repaired behavior.
    rt.execute('pre_safe=Colonist.GetExpeditionReturnDome; u,h=subject(true,false); h.invalid=true; test_domes={}; test_safety=home(); test_safety.kind="Dome"; test_safety.ui_working=false')
    b.check('pre-C102 fallback is dead dome', rt.eval('pre_safe(u,{})==nil and ChooseDome(u,{},test_safety)==test_safety'))
    rt.execute(ARRIVAL.read_text(encoding='utf-8'))
    rt.execute('assert(SMRFixPack.defs.ArrivalDeaths.apply()==nil)')
    rt.execute('safe=home(); safe.kind="Dome"; far=home(); far.kind="Dome"; test_domes={far,safe}; test_dist={[safe]=10,[far]=20}')
    b.check('shipped chooser keeps dead fallback when live alternatives full', rt.eval('ChooseDome(u,test_domes,test_safety)==test_safety'))
    b.check('C102 selects nearest live alternative to dead fallback', rt.eval('u:GetExpeditionReturnDome({})==safe'))
    for receiver in ['new', 'legacy']:
        rt.execute('safe.free=1; u,h=subject(true,false); h.ui_working=false; rocket=u.holder; rocket.city=u.city; rocket.transported_passengers={u}; rocket.cargo={any_specialization={amount=1}}; setmetatable(rocket,{__index=CargoTransporterNew})')
        rt.execute('rocket:UnloadPassengers()' if receiver=='new' else 'RocketBase.Disembark(rocket,{u})')
        b.check('C102 '+receiver+' corrects before fallback reservation', rt.eval('u.reserved_residence==safe and not h.reserved[u] and u.issued[3]==safe'))
    rt.execute('u.expedition_residence=home(); u.expedition_residence.kind="Dome"; u.expedition_residence.ui_working=false')
    b.check('C102 ordinary dome returnee also selects safe fallback', rt.eval('u:GetExpeditionReturnDome({})==safe'))
    rt.execute('test_domes={}; test_dist={}; u:GetExpeditionReturnDome({}); u:GetExpeditionReturnDome({})')
    b.check('C102 no alternative preserves vanilla and logs once', rt.eval('u:GetExpeditionReturnDome({})==nil and SMRFixPack.logs==1'))
    rt.execute('u,h=subject(true,false); test_domes={}; test_dist={}')
    b.check('C102 composed with C95 retains held full habitat', rt.eval('u:GetExpeditionReturnDome({})==h'))
    rt.execute('before=Colonist.GetExpeditionReturnDome; SMRFixPack.defs.ArrivalDeaths.apply()')
    b.check('arrival apply idempotent', rt.eval('before==Colonist.GetExpeditionReturnDome'))
    for receiver in ['CargoTransporterNew', 'RocketBase']:
        solo=runtime()
        solo.execute(receiver+'=nil')
        solo.execute(ARRIVAL.read_text(encoding='utf-8'))
        solo.execute('assert(SMRFixPack.defs.ArrivalDeaths.apply()==nil)')
        solo.execute(MODULE.read_text(encoding='utf-8'))
        solo.execute('assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil); u,h=subject(true,false); test_domes={}; test_safety=false; rocket=u.holder; rocket.city=u.city; rocket.transported_passengers={u}; rocket.cargo={any_specialization={amount=1}}')
        solo.execute('RocketBase.Disembark(rocket,{u})' if receiver=='CargoTransporterNew' else 'CargoTransporterNew.UnloadPassengers(setmetatable(rocket,{__index=CargoTransporterNew}))')
        b.check(receiver+' absent: other receiver still reserves and dispatches home', solo.eval('u.reserved_residence==h and u.issued[3]==h'))
    return b.finish('DESK ONLY; live travel and removal require engine evidence')


if __name__ == '__main__':
    raise SystemExit(main())
