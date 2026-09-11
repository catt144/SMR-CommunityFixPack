#!/usr/bin/env python3
"""F73 wrapper control only. No engine, no full Idle simulation, no colony reach claim.

Load the whole current module over a finite Idle spy. SetCommand raises a named
sentinel because engine SetCommand terminates the caller; a returning stub would
falsely allow the original Idle to run after the shelter command.
"""
import deskbench as db
from desk_migration_cluster import runtime, module


def main():
    b = db.Bench('F73 shelter wrapper: branch and stand-down controls only')
    rt = runtime()
    rt.execute('''
      now=1000; breathable=false; original_calls=0
      GameTime=function() return now end
      GetAtmosphereBreathable=function() return breathable end
      g_Consts.OxygenMaxOutsideTime=100; const.HourDuration=60
      Colonist.Idle=function() original_calls=original_calls+1 end
      function subject()
        return setmetatable({outside_start=950,residence={working=true},
          GetMap=function() return {} end, IsDying=function(self) return self.dying end,
          SetCommand=function(self,cmd) self.command=cmd; error("COMMAND_TERMINATED") end},
          {__index=Colonist})
      end
      c=subject(); c:Idle()
    ''')
    b.check('module-absent control calls original Idle and supplies no Rest command',
            rt.eval('original_calls==1 and c.command==nil'))
    module(rt, 'ShelterReflex')
    rt.execute('c=subject(); original_calls=0; ok,err=pcall(c.Idle,c)')
    b.check('half-budget vacuum condition sends Rest and does not call original',
            rt.eval('not ok and string.find(err,"COMMAND_TERMINATED") and c.command=="Rest" and original_calls==0 and c.SMRFixPack_shelter_try==now'))
    cases = [
        ('below half budget', 'c.outside_start=951'),
        ('no residence', 'c.residence=false'),
        ('nonworking residence', 'c.residence.working=false'),
        ('transport task present', 'c.transport_task={}'),
        ('dying colonist', 'c.dying=true'),
        ('no outside timer', 'c.outside_start=false'),
        ('retry throttle', 'c.SMRFixPack_shelter_try=now-59'),
        ('breathable atmosphere', 'breathable=true'),
    ]
    for label, setup in cases:
        rt.execute('breathable=false; c=subject(); original_calls=0; ' + setup + '; c:Idle()')
        b.check(label + ': original Idle runs, no shelter command',
                rt.eval('original_calls==1 and c.command==nil'))
    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
