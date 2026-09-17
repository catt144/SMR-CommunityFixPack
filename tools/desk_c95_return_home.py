#!/usr/bin/env python3
"""Registered C95 return repair, extracted shipped selector/dispatcher controls.

Synthetic route answers do not measure pathfinding. CommandObject.SetCommand
records dispatch instead of starting engine threads. Housing/trait/life-support
predicates are explicit fixture inputs, with rejection legs. The shipped
ReturnFromExpedition body runs synchronously with inert animation/destructor
stubs, so its own tail issues the TransportByFoot order the placement reads.
No serialization, colony creation, animation or travel timing is simulated.

C95_RETURN_MODULE=<path> loads a scratch variant of the module instead, so a
falsification run can require the right legs to FAIL.
"""
from pathlib import Path
import hashlib
import os
import re
import subprocess

from deskbench import ENGINE_SHIMS, REPO, body, load_at, Bench, lua_runtime

MODULE = Path(os.environ.get('C95_RETURN_MODULE') or Path(REPO, 'Code/Fix_HabitatExpeditionReturn.lua'))
ARRIVAL = Path(REPO, 'Code/Fix_ArrivalDeaths.lua')
SOURCES = [
    ('Lua/_GameUtils.lua', 'ChooseDome'),
    ('Lua/Units/Colonist.lua', 'Colonist:GetExpeditionReturnDome'),
    ('Lua/Units/Colonist.lua', 'Colonist:ReturnFromExpedition'),
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
    Colonist={}; Residence={}; CommandObject={}; TransportTicket={}; WaypointsObj={}
    CargoTransporterNew={}; RocketBase={}; Community={}; MicroGHabitatBase={}
    function IsValid(x) return type(x)=='table' and not x.invalid end
    function IsKindOf(x,k) return IsValid(x) and x.kind==k end
    function IsSameMap(a,b) return a.map==b.map end
    -- A position is a table; its walk flag answers "in walking range of the home".
    function IsInWalkingDist(home,origin,city) return origin.walk end
    function GetTransportRoute(origin,home,check_use,allow_reachable)
      if origin.train and origin.map==home.map then return {station=1},{station=2} end
    end
    function GameTime() return 100 end
    function Sleep() end
    function AddObjectToNotification(obj) obj.confused=true end
    SessionRandom={Random=function() return 0 end}
    function GetSortedColonistSpecializationTable() return {} end
    function ripairs(t)
      local i=#t+1; return function() i=i-1; if i>0 then return i,t[i] end end
    end
    function Colonist:Idle() end
    function Colonist:OnArrival() end
    function Colonist:Arrive() end
    function Colonist:TransportByFoot() end
    function WaypointsObj:GetEntrancePoints() end
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
      self.issued={cmd,a,b}; self.issued_at=self.pos; return 'issued',nil,'tail'
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
    -- Inert engine surface for the extracted ReturnFromExpedition body.
    function Colonist:GetPos() return self.pos end
    function Colonist:IsValidPos() return self.pos~=nil end
    function Colonist:SetPos(p) self.pos=p end
    function Colonist:SetHolder(h) self.holder=h end
    function Colonist:Random(a,b) return a end
    function Colonist:SetAngle() end
    function Colonist:SetOutside() end
    function Colonist:SetDisembarkAnim() end
    function Colonist:TimeToAnimEnd() return 0 end
    function Colonist:Detach() end
    function Colonist:SetState() end
    function Colonist:GetMap() return self.map end
    function Colonist:CancelWorkReservation() end
    function Colonist:PushDestructor(f) self.dtors=self.dtors or {}; self.dtors[#self.dtors+1]=f end
    function Colonist:PopAndCallDestructor()
      local f=table.remove(self.dtors); if f then f(self) end
    end
    function home()
      return setmetatable({kind='MicroGHabitatBase', map=1, ui_working=true,
        accept_colonists=true, support=true, visit=true, suitable=true,
        entrances={{door=1,walk=true},{door=2,walk=true}},
        GetScoreFor=function() return 100 end,
        HasFreeLivingSpaceFor=function(s) return s.free>0 end,
        CanAcceptNewColonists=function(s) return s.accept_colonists and s.ui_working end,
        reserved={}, free=0, colonists={},
        HasLifeSupport=function(s) return s.support end,
        CanVisit=function(s,u) return s.visit end,
        IsSuitable=function(s,u) return s.suitable end,
        GetFreeSpace=function(s) return s.free end,
        GetEntrancePoints=function(s,t) return s.entrances end,
        ChooseResidence=function(s,u) return s.suitable and s or false end,
      },{__index=Residence})
    end
    function rocket_at(walk,train)
      return {walk=walk,train=train,map=1,
        IsValidPos=function() return true end,
        GetPos=function(s) return s end,
        GetSpotBeginIndex=function() return 1 end,
        GetSpotLoc=function(s) return s,0 end}
    end
    function subject(walk,train)
      local h=home()
      local u=setmetatable({traits={},city={},map=1,holder=rocket_at(walk,train),
        expedition_residence=h, reserved_residence=h}, {__index=Colonist})
      h.reserved[1]=u; h.reserved[u]=true
      return u,h
    end
    -- The receiver's order, then the command body it issues, in one frame.
    function land(u,rocket)
      rocket=rocket or u.holder
      rocket.city=u.city; rocket.transported_passengers={u}
      rocket.cargo={any_specialization={amount=1}}
      setmetatable(rocket,{__index=CargoTransporterNew})
      rocket:UnloadPassengers()
      local order=u.issued
      if order and order[1]=='ReturnFromExpedition' then
        Colonist.ReturnFromExpedition(u,order[2],order[3])
      end
      return order
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
    print('MODULE', MODULE, 'sha256:', hashlib.sha256(MODULE.read_bytes()).hexdigest())
    for rel, selector in SOURCES:
        text, first, last = body(rel, '^function ' + re.escape(selector) + r'\(')
        canonical = '\n'.join(line.rstrip() for line in text.splitlines())
        print('SOURCE', rel, selector, f'lines={first}-{last} count={last-first+1}',
              'sha256=' + hashlib.sha256(canonical.encode()).hexdigest())
    source = MODULE.read_text(encoding='utf-8')
    b = Bench('C95/C102 registered return repair (desk only)')

    # Harm controls on the pre-fix bodies: vanilla selector, dispatcher and return body.
    rt = runtime()
    rt.execute('u,h=subject(false,false)')
    b.check('pre-fix: vanilla selector loses out-of-reach habitat', rt.eval('u:GetExpeditionReturnDome({}) == nil'))
    rt.execute('u,h=subject(false,true)')
    rt.execute("Colonist.SetCommand(u,'ReturnFromExpedition',u.holder,h)")
    b.check('pre-fix: vanilla dispatcher already books arrival train', rt.eval(
        "u.issued[1]=='DisembarkOnArrival' and u.transport_ticket.reason=='MigrateByTrain'"
        " and u.transport_ticket.destination==h and u.transport_ticket.param==false"))
    rt.execute('u,h=subject(false,false); wrong=home(); wrong.free=1; wrong:ReserveResidence(u)')
    b.check('pre-fix: fallback reservation erases expedition home before return', rt.eval(
        'u.reserved_residence==wrong and u.expedition_residence==false and not h.reserved[u]'))
    rt.execute('u,h=subject(false,false); rocket=u.holder; Colonist.ReturnFromExpedition(u,rocket,h)')
    b.check('pre-fix: shipped return body walks from the rocket to a far home', rt.eval(
        "u.issued[1]=='TransportByFoot' and u.issued[2]==h and u.issued_at==rocket and u.expedition_residence==false"))

    rt.execute(source)
    rt.execute("assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil)")

    # Selector admission: the route no longer matters, usability still does.
    for label, walk, train in [('walk', True, False), ('rail', False, True), ('no route', False, False)]:
        rt.execute(f'u,h=subject({str(walk).lower()},{str(train).lower()}); candidates={{}}; chosen=u:GetExpeditionReturnDome(candidates)')
        b.check(label + ': held usable home admitted', rt.eval('chosen==h'))
        b.check(label + ': shared input not mutated', rt.eval('#candidates==0'))
    for label, setup in [
        ('destroyed', 'h.invalid=true'), ('closed', 'h.ui_working=false'),
        ('refuses arrivals', 'h.accept_colonists=false'), ('no life support', 'h.support=false'),
        ('cannot visit', 'h.visit=false'), ('player filter now forbids them', 'h.suitable=false'),
        ('reservation lost', 'u.reserved_residence=false'), ('different map', 'h.map=2'),
    ]:
        rt.execute('u,h=subject(false,false); ' + setup)
        b.check(label + ': delegates without admitting home', rt.eval('u:GetExpeditionReturnDome({})==nil'))
    rt.execute('u,h=subject(true,false); h.kind="Dome"; candidates={h}')
    b.check('ordinary dome return preserved', rt.eval('u:GetExpeditionReturnDome(candidates)==h'))
    rt.execute('u,h=subject(true,false); candidates={h}')
    b.check('already reachable home preserved', rt.eval('u:GetExpeditionReturnDome(candidates)==h and #candidates==1'))

    # Required: an out-of-reach home placed, through both receivers and the shipped body.
    for receiver in ['new', 'legacy']:
        rt.execute('u,h=subject(false,false); test_domes={}; test_safety=false; rocket=u.holder')
        if receiver == 'new':
            rt.execute('land(u)')
        else:
            rt.execute('RocketBase.Disembark(rocket,{u}); Colonist.ReturnFromExpedition(u,u.issued[2],u.issued[3])')
        b.check(receiver + ': out-of-reach home placed at its own entrance before the walk order', rt.eval(
            "u.issued[1]=='TransportByFoot' and u.issued[2]==h and u.issued_at==h.entrances[1] and u.pos==h.entrances[1]"))
        b.check(receiver + ': placed returnee keeps the held bed, hold released natively', rt.eval(
            'u.reserved_residence==h and h.reserved[u] and u.expedition_residence==false'))
    # Required: in range, still walked.
    rt.execute('u,h=subject(true,false); test_domes={}; test_safety=false; rocket=u.holder; land(u)')
    b.check('in-range home still walked from the rocket, not placed', rt.eval(
        "u.issued[1]=='TransportByFoot' and u.issued[2]==h and u.issued_at==rocket and u.reserved_residence==h"))
    # Rail stays vanilla's: the booking is untouched, and its final walk starts in range.
    rt.execute('u,h=subject(false,true); test_domes={}; test_safety=false; rocket=u.holder; land(u)')
    b.check('rail: native train booking to the held home untouched', rt.eval(
        "u.issued[1]=='DisembarkOnArrival' and u.transport_ticket.destination==h and u.pos==nil"))
    rt.execute('u.holder=false; station={walk=true,map=1}; u.pos=station; u:SetCommand("TransportByFoot",h)')
    b.check('rail: walk from the arrival station is not placed', rt.eval('u.issued_at==station'))
    # The mark is consumed once and does not leak into later orders.
    rt.execute('u,h=subject(false,false); u:GetExpeditionReturnDome({}); u.holder=false; u.pos={walk=false,map=1}')
    rt.execute('first=u.pos; u:SetCommand("Idle")')
    b.check('mark survives an unrelated order', rt.eval("u.issued[1]=='Idle' and u.pos==first"))
    rt.execute('other=home(); u:SetCommand("TransportByFoot",other)')
    b.check('walk order to another destination consumes the mark without placing', rt.eval('u.pos==first'))
    rt.execute('u:SetCommand("TransportByFoot",h)')
    b.check('consumed mark does not place a later walk home', rt.eval('u.pos==first'))
    # Placement-time guards decline to vanilla's walk.
    for label, setup in [
        ('home destroyed in the animation', 'h.invalid=true'),
        ('reservation cancelled in the animation', 'u.reserved_residence=false'),
        ('still in a holder', 'u.holder=rocket_at(false,false)'),
        ('home has no entrance points', 'h.entrances=nil'),
        ('home became unusable', 'h.support=false'),
    ]:
        rt.execute('u,h=subject(false,false); u:GetExpeditionReturnDome({}); u.holder=false; start={walk=false,map=1}; u.pos=start; '
                   + setup + '; u:SetCommand("TransportByFoot",h)')
        b.check(label + ': walks, order still issued', rt.eval("u.issued[1]=='TransportByFoot' and u.pos==start"))
    rt.execute('u,h=subject(false,false); u:GetExpeditionReturnDome({}); u.holder=false; start={walk=false,map=1}; u.pos=start;'
               ' h.GetEntrancePoints=function() local absent=nil; return absent.fail end; logs=SMRFixPack.logs;'
               ' result=table.pack(u:SetCommand("TransportByFoot",h))')
    b.check('placement error: order issued, returns preserved, logged', rt.eval(
        "u.issued[1]=='TransportByFoot' and u.pos==start and result.n==3 and result[1]=='issued' and result[3]=='tail' and SMRFixPack.logs==logs+1"))
    rt.execute('result=table.pack(u:SetCommand("Work",nil,nil,7))')
    b.check('command wrapper preserves nil-bearing tuple for everyone', rt.eval("result.n==3 and result[1]=='issued' and result[2]==nil"))

    # Required: no habitat expedition hold, including a fresh arrival, untouched.
    far = 'far=home(); far.reserved={}'
    for label, setup in [
        ('Earth arrival reserved into a far habitat', 'c=setmetatable({traits={},city={},map=1,arriving=true,command="Arrive"},{__index=Colonist}); far:ReserveResidence(c)'),
        ('migrant with a reserved habitat', 'c=setmetatable({traits={},city={},map=1},{__index=Colonist}); far:ReserveResidence(c)'),
        ('dome resident returnee', 'c=setmetatable({traits={},city={},map=1,expedition_residence={kind="Residence"}},{__index=Colonist})'),
    ]:
        rt.execute(far + '; far.free=1; ' + setup + '; c.pos={walk=false,map=1}; start=c.pos; c:SetCommand("TransportByFoot",far)')
        b.check(label + ': never placed', rt.eval("c.issued[1]=='TransportByFoot' and c.pos==start"))
    rt.execute(far + '; far.free=1; recruit=setmetatable({traits={},city={},map=1,arriving=true,holder=rocket_at(false,false)},{__index=Colonist});'
               ' test_domes={far}; test_safety=false; land(recruit)')
    b.check('covert-ops recruit (no hold) via receiver and body: not placed', rt.eval(
        "recruit.issued[1]=='TransportByFoot' and recruit.issued[2]==far and recruit.issued_at==recruit.appear_location"))

    # Mark is memory only: a reload between landing and the walk order walks the held home.
    reload2 = runtime()
    reload2.execute(source)
    reload2.execute('assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil); u,h=subject(false,false); rocket=u.holder;'
                    ' Colonist.ReturnFromExpedition(u,rocket,h)')
    b.check('reload residual: unmarked returnee walks to the still-held home', reload2.eval(
        "u.issued[1]=='TransportByFoot' and u.issued_at==rocket and u.reserved_residence==h"))

    rt.execute('u,h=subject(false,false); h.free_spaces={inclusive=0}; h.CanVisit=MicroGHabitatBase.CanVisit')
    b.check('shipped full-habitat gate rejects anonymous visitor', rt.eval('not h:CanVisit()'))
    b.check('shipped full-habitat gate accepts its reserved returnee', rt.eval('h:CanVisit(u)'))
    b.check('module also restores full habitat omitted by CanVisit', rt.eval('u:GetExpeditionReturnDome({})==h'))
    rt.execute('u,h=subject(true,false); u.dome=h; result=table.pack(u:UpdateWorkplace())')
    b.check('housing precedes picker at rejoin', rt.eval('u.residence==h and not u.hired_in_dome and u.work_calls==1'))
    b.check('work wrapper preserves nil-bearing return tuple', rt.eval('result.n==3 and result[1]=="work" and result[2]==nil and result[3]=="tail"'))
    rt.execute('u,h=subject(true,false); u.dome={}; u:UpdateWorkplace()')
    b.check('foreign dome does not get reassigned', rt.eval('u.residence==nil and u.work_calls==1'))
    rt.execute('u,h=subject(true,false); u.dome=h; u.blocked=true; u:UpdateWorkplace()')
    b.check('housing allocator refusal is respected (known gap)', rt.eval('u.residence==nil and u.work_calls==1'))
    code = '\n'.join(line for line in source.splitlines() if not line.lstrip().startswith('--'))
    b.check('module adds no persisted state or yielding body', not re.search(
        r'\b(?:GameVar|CreateGameTimeThread|CreateRealTimeThread|Sleep|WaitMsg|SetResidence|PersistableGlobals)\s*\(', code))
    for shape in ['nil', '{kind="Dome"}', '{kind="Residence"}', '{kind="Other"}']:
        delegated=runtime()
        delegated.execute("calls=0; function Colonist:GetExpeditionReturnDome(d,...) calls=calls+1; seen=d; return false,nil,'tail',... end")
        delegated.execute(source)
        delegated.execute('assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil); u,h=subject(true,false); u.expedition_residence='+shape+"; candidates={}; result=table.pack(u:GetExpeditionReturnDome(candidates,42,nil))")
        b.check('non-habitat '+shape+' delegates exact arguments and returns', delegated.eval("calls==1 and seen==candidates and result.n==5 and result[1]==false and result[3]=='tail' and result[4]==42"))
    rt.execute("before=Colonist.GetExpeditionReturnDome; before_cmd=Colonist.SetCommand; SMRFixPack.defs.HabitatExpeditionReturn.apply()")
    b.check('return apply idempotent', rt.eval('before==Colonist.GetExpeditionReturnDome and before_cmd==Colonist.SetCommand'))
    # Save the pre-C102 selector as the harm control; do not base it on repaired behavior.
    rt.execute('pre_safe=Colonist.GetExpeditionReturnDome; u,h=subject(true,false); h.invalid=true; test_domes={}; test_safety=home(); test_safety.kind="Dome"; test_safety.ui_working=false')
    b.check('pre-C102 fallback is dead dome', rt.eval('pre_safe(u,{})==nil and ChooseDome(u,{},test_safety)==test_safety'))
    rt.execute(ARRIVAL.read_text(encoding='utf-8'))
    rt.execute('assert(SMRFixPack.defs.ArrivalDeaths.apply()==nil)')
    rt.execute('safe=home(); safe.kind="Dome"; far=home(); far.kind="Dome"; test_domes={far,safe}; test_dist={[safe]=10,[far]=20}')
    b.check('shipped chooser keeps dead fallback when live alternatives full', rt.eval('ChooseDome(u,test_domes,test_safety)==test_safety'))
    b.check('C102 selects nearest live alternative to dead fallback', rt.eval('u:GetExpeditionReturnDome({})==safe'))
    for receiver in ['new', 'legacy']:
        rt.execute('safe.free=1; u,h=subject(false,false); h.ui_working=false; rocket=u.holder; rocket.city=u.city; rocket.transported_passengers={u}; rocket.cargo={any_specialization={amount=1}}; setmetatable(rocket,{__index=CargoTransporterNew})')
        rt.execute('rocket:UnloadPassengers()' if receiver=='new' else 'RocketBase.Disembark(rocket,{u})')
        b.check('C102 '+receiver+': unusable home falls to nearest safe dome before reservation', rt.eval('u.reserved_residence==safe and not h.reserved[u] and u.issued[3]==safe'))
        rt.execute('Colonist.ReturnFromExpedition(u,u.issued[2],u.issued[3])')
        b.check('C102 '+receiver+': fallback returnee walks, not placed', rt.eval("u.issued[1]=='TransportByFoot' and u.issued[2]==safe and u.issued_at==rocket"))
    rt.execute('u.expedition_residence=home(); u.expedition_residence.kind="Dome"; u.expedition_residence.ui_working=false')
    b.check('C102 ordinary dome returnee also selects safe fallback', rt.eval('u:GetExpeditionReturnDome({})==safe'))
    rt.execute('test_domes={}; test_dist={}; logs=SMRFixPack.logs; u:GetExpeditionReturnDome({}); u:GetExpeditionReturnDome({})')
    b.check('C102 no alternative preserves vanilla and logs once', rt.eval('u:GetExpeditionReturnDome({})==nil and SMRFixPack.logs==logs+1'))
    rt.execute('u,h=subject(false,false); test_domes={}; test_dist={}; test_safety=false; rocket=u.holder; land(u)')
    b.check('C102 composed with C95: far held habitat retained and placed', rt.eval('u.reserved_residence==h and u.issued_at==h.entrances[1]'))
    rt.execute('before=Colonist.GetExpeditionReturnDome; SMRFixPack.defs.ArrivalDeaths.apply()')
    b.check('arrival apply idempotent', rt.eval('before==Colonist.GetExpeditionReturnDome'))
    for receiver in ['CargoTransporterNew', 'RocketBase']:
        solo=runtime()
        solo.execute(receiver+'=nil')
        solo.execute(ARRIVAL.read_text(encoding='utf-8'))
        solo.execute('assert(SMRFixPack.defs.ArrivalDeaths.apply()==nil)')
        solo.execute(source)
        solo.execute('assert(SMRFixPack.defs.HabitatExpeditionReturn.apply()==nil); u,h=subject(false,false); test_domes={}; test_safety=false; rocket=u.holder; rocket.city=u.city; rocket.transported_passengers={u}; rocket.cargo={any_specialization={amount=1}}')
        solo.execute('RocketBase.Disembark(rocket,{u})' if receiver=='CargoTransporterNew' else 'CargoTransporterNew.UnloadPassengers(setmetatable(rocket,{__index=CargoTransporterNew}))')
        solo.execute('Colonist.ReturnFromExpedition(u,u.issued[2],u.issued[3])')
        b.check(receiver+' absent: other receiver still reserves and places home', solo.eval('u.reserved_residence==h and u.issued_at==h.entrances[1]'))
    return b.finish('DESK ONLY; live travel and removal require engine evidence')


if __name__ == '__main__':
    raise SystemExit(main())
