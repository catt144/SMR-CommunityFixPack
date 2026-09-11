#!/usr/bin/env python3
"""Extracted topology controls. Engine geometry/buildability is NOT exercised.

No fix is installed. Station connector pairing and service eligibility are named
fixtures; real route construction, enumeration and dome adjacency bodies run.
"""
import deskbench as db
from desk_migration_cluster import runtime, shipped


def main():
    b = db.Bench('Migration observations: supplied topology, no in-play reproduction')
    rt = runtime()
    rt.execute('''
      PassageBase={}; g_MediaCenterWorkingCheckVersion=0; g_ClusterWorkplacesVersion=0
      IsBeingDestructed=function() return false end; Msg=function() end
      function newdome()
        local d=setmetatable({connected_version=0,labels={interestShopping={}},
          allow_service_in_connected=true,accept_colonists=true},{__index=Dome})
        d:InitPassageTables(); return d
      end
      ServiceFailure={NotFound=1,None=-1}
    ''')
    for p in ['InitPassageTables', 'UpdateConnectedNetwork', 'GetClusterDomes',
              'GetResidentServiceDomes', 'GetService']:
        shipped(rt, 'Lua/Buildings/Dome.lua', '^function Dome:' + p + r'\(')
    for p in ['ConnectDomePair', 'ConnectDomeToHub']:
        shipped(rt, 'Lua/Passage.lua', '^function PassageBase:' + p + r'\(')
    shipped(rt, 'Lua/ServiceBase.lua', r'^function GetMaxPerformanceAvailableServiceInDome\(')
    rt.execute('''
      a=newdome(); d=newdome(); c=newdome()
      PassageBase:ConnectDomePair(a,d); PassageBase:ConnectDomePair(d,c)
      shopper={Random=function() return 0 end}
      shop={CanBeUsedBy=function() return true,-1 end,GetEffectivePerformance=function() return 100 end}
      c.labels.interestShopping={shop}
    ''')
    b.check('F62 ordinary A-B-C chain: network includes C, service candidates do not',
            rt.eval('a.dome_network[c] and not a.connected_domes[c] and not a:GetService("interestShopping",shopper)'))
    rt.execute('''
      hub={hub_domes={}}; a=newdome(); d=newdome(); c=newdome()
      PassageBase:ConnectDomeToHub(a,hub); PassageBase:ConnectDomeToHub(d,hub)
      PassageBase:ConnectDomeToHub(c,hub); c.labels.interestShopping={shop}
    ''')
    b.check('F62 Passage Hub connects its spokes pairwise and offers C service to A',
            rt.eval('a.connected_domes[c] == 1 and a:GetService("interestShopping",shopper) == shop'))
    rt.execute('a.accept_colonists=false; c.accept_colonists=false')
    b.check('F61 selector has no own/destination quarantine gate with eligible-service fixture',
            rt.eval('a:GetService("interestShopping",shopper) == shop'))
    rt.execute('a.allow_service_in_connected=false')
    b.check('F61/F62 service-passage switch still excludes remote service',
            rt.eval('not a:GetService("interestShopping",shopper)'))

    rt = runtime()
    rt.execute('''
      const={trfInclusive=1,trfPassengerTransport=2,trfBidirectional=4,trfRunnableOnly=8}
      IsBeingDestructed=function() return false end
      GetNextConnectedStation=function(s) return s end -- no tunnel fixture
      table.find=function(t,v) for i,x in ipairs(t) do if x==v then return i end end end
      function station(name)
        return {name=name,working=true,links={},
          GetConnectedTrack=function(self,t) return self.links[t] end}
      end
      function track(a,b)
        return {elements={1},elements_under_construction={},transport_mode='all',
          CanTrainsRun=function() return true end,
          GetDestStation=function(self,s) if s==a then return b else return a end end}
      end
      a=station('A'); b=station('B'); c=station('C');
      ab=track(a,b); bc=track(b,c); ca=track(c,a)
      a.links={[ab]=ca,[ca]=ab}; b.links={[ab]=bc,[bc]=ab}; c.links={[bc]=ca,[ca]=bc}
    ''')
    shipped(rt, 'Lua/TrainTransport.lua', r'^function EnumRouteTracks\(')
    src, line, _ = db.body('Lua/TrainTransport.lua', r'^function ForEachStationAlongTrack\(')
    db.load_at(rt, 'local stations_visited\n' + src, '=Lua/TrainTransport.lua', line - 1)
    rt.execute('''
      route=EnumRouteTracks(a,ab)
      city={train_track_routes={[ab]=route,[bc]=route,[ca]=route}}
      a.city=city; b.city=city; c.city=city
      function visits(s,t,flags)
        local out={}; ForEachStationAlongTrack(s,t,flags or 0,function(d) out[#out+1]=d.name end)
        return table.concat(out,',')
      end
    ''')
    b.check('F80 real builder produces a three-station loop from paired-connector fixture',
            rt.eval('route.loop and #route==3 and #route.edges==3 and route[1]==a and route[3]==c'))
    b.check('F80 loop seam C->A uses stride -2 and omits B on that departure track',
            rt.eval('visits(c,ca)=="A"'))
    b.check('F80 ordinary forward direction covers both remaining loop stations',
            rt.eval('visits(a,ab)=="B,C"'))
    b.check('F80 opposite track from C covers B and A: union can hide per-track omission',
            rt.eval('visits(c,bc)=="B,A"'))
    rt.execute('bc.transport_mode="cargo"')
    b.check('F80 passenger flag correctly truncates a cargo-only edge',
            rt.eval('visits(a,ab,const.trfPassengerTransport)=="B"'))
    rt.execute('bc.transport_mode="all"; a.links[ab]=nil; c.links[bc]=nil; route=EnumRouteTracks(a,ab); city.train_track_routes[ab]=route; city.train_track_routes[bc]=route')
    b.check('F80 open-line control visits both destinations without loop seam',
            rt.eval('not route.loop and visits(a,ab)=="B,C" and visits(c,bc)=="B,A"'))
    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
