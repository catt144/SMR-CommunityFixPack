#!/usr/bin/env python3
"""F59: immediate vacancy notification can steal an expedition home.

Runs extracted Colonist.EnterTransporter -> SetDome -> SetResidence, followed by
extracted OnDisappear, with real residence selection/reservation bodies and whole
F59/F58 modules. Unit.EnterTransporter is a named engine-boundary stub: it marks
disappeared and calls OnDisappear (the real path goes via Unit.Disappear).
Labels, UI, comfort, geometry and trait-free suitability are fixtures. No claim
about engine timing, real expedition completion, or in-play reproduction.
"""
import deskbench as db
from desk_migration_cluster import runtime, shipped, module


def scenario(patched, waiting=True, stale_sweep=False, action='expedition', candidate=False):
    rt = runtime()
    rt.execute('''
      Unit={OnDisappear=function() end,
        EnterTransporter=function(self) self.disappeared=true; self:OnDisappear() end}
      function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
      IsKindOf=function(o,c) return type(o)=="table" and o.kind==c end
      Msg=function() end; RebuildInfopanel=function() end
      UpdateAttachedSign=function() end
      GameTime=function() return 100 end
      min_int=-999999; GetResidenceComfort=function() return 50,0 end
      TraitPresets={}; ColonistFilterFunc={}
      g_Consts.ForcedByUserLockTimeout=3600000
    ''')
    for method in ['EnterTransporter','SetDome','SetResidence','UpdateResidence',
                   'CancelResidenceReservation','CanChangeCommand','OnDisappear']:
        shipped(rt, 'Lua/Units/Colonist.lua', '^function Colonist:' + method + r'\(')
    for method in ['AddResident','RemoveResident','GetFreeSpace','CanReserveResidence',
                   'ReserveResidence','CancelResidenceReservation','CheckHomeForHomeless','IsSuitable']:
        shipped(rt, 'Lua/Buildings/Residence.lua', '^function Residence:' + method + r'\(')
    shipped(rt, 'Lua/Buildings/Residence.lua', r'^function ChooseResidence\(')
    shipped(rt, 'Lua/Buildings/Dome.lua', r'^function Dome:ChooseResidence\(')
    if patched:
        if candidate:
            # AUDIT IDEA ONLY. Transform an in-memory copy, never the Code file.
            # Capture the exact departing expedition home before orig can mutate it.
            from pathlib import Path
            text = db.read(Path(db.REPO) / 'Code' / 'Fix_FreedHousingNotice.lua')
            needle = 'local left = self.residence'
            assert text.count(needle) == 1
            text = text.replace(needle, needle + '\n\t\t\tlocal expedition_home = left and self.expedition_residence == left')
            needle = 'if left and left ~= self.residence and IsValid(left)'
            assert text.count(needle) == 1
            text = text.replace(needle, 'if not expedition_home and left and left ~= self.residence and IsValid(left)')
            db.load_at(rt, text, '=F59_UNBUILT_IDEA')
            rt.execute('assert(modules.FreedHousingNotice.apply() == nil)')
        else:
            module(rt, 'FreedHousingNotice')
    if stale_sweep:
        module(rt, 'StaleReservations')
    rt.execute('''
      local noop=function() end
      dome={working=true,ui_working=true,labels={Homeless={}},
        ResetFreeSpace=noop, ChooseResidence=Dome.ChooseResidence,
        RemoveFromLabel=function(self,label,c) table.remove_entry(self.labels[label] or {},c) end}
      home=setmetatable({parent_dome=dome,working=true,ui_working=true,capacity=1,closed=0,
        filter_residents="Everyone",colonists={},reserved={},UpdateOccupation=noop}, {__index=Residence})
      dome.labels.Residence={home}
      city={labels={Residence={home}}}; MainCity=city
      local function colonist()
        return setmetatable({dome=dome,city=city,traits={},residence=false,reserved_residence=false,
          CanVote=function() return false end, SetWorkplace=noop,
          UpdateHomelessLabels=function(self)
            if self.residence then table.remove_entry(dome.labels.Homeless,self) end
          end,
          UpdateLowComfortNotification=noop, UpdateMorale=noop, IsTransported=function() return false end,
          CheckForcedResidence=function() return false end, ClearDetrimentalStatusEffects=noop,
          ClearTransportRequest=Colonist.CancelResidenceReservation, AssignToService=noop, SetOutside=noop},
          {__index=Colonist})
      end
      crew=colonist(); crew.residence=home; home.colonists={crew}
      homeless=colonist()
    ''')
    if waiting:
        rt.execute('dome.labels.Homeless={homeless}')
    if action == 'expedition':
        rt.execute('crew:EnterTransporter({expedition=true})')
    elif action == 'ordinary':
        rt.execute('crew:SetDome(false)')
    elif action == 'unrelated_hold':
        rt.execute('crew.expedition_residence={}; crew:SetDome(false)')
    else:
        raise ValueError(action)
    return rt


def main():
    b = db.Bench('F59 expedition hold: same shipped sequence, module off/on controls')
    rt = scenario(False)
    b.check('vanilla: crew retains reserved home with a homeless neighbour',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home and home.reserved[crew] == true and homeless.residence == false'))
    rt = scenario(True)
    b.check('F59 applied: neighbour takes bed and expedition hold is lost',
            rt.eval('homeless.residence == home and crew.expedition_residence == false and crew.reserved_residence == false and not home.reserved[crew]'))
    b.check('F59 applied: residence remains within capacity (this is loss of hold, not overflow)',
            rt.eval('#home.colonists == 1 and #home.reserved == 0'))
    rt = scenario(True, waiting=False)
    b.check('negative control: F59 preserves crew home when no neighbour competes',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home'))
    rt = scenario(True, stale_sweep=True)
    b.check('current F58 exemption cannot protect a hold F59 prevented from being created',
            rt.eval('homeless.residence == home and crew.expedition_residence == false and crew.reserved_residence == false'))
    rt.execute('OnMsg.NewDay()')
    b.check('F58 daily sweep does not restore the missing hold',
            rt.eval('homeless.residence == home and crew.reserved_residence == false'))
    rt = scenario(False, action='ordinary')
    b.check('original F59 gap: vanilla ordinary departure leaves an eligible neighbour homeless beside a free bed',
            rt.eval('home:GetFreeSpace() == 1 and homeless.residence == false'))
    rt.execute('homeless:UpdateResidence()')
    b.check('original-gap control: a later housing update takes that same bed',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, action='ordinary')
    b.check('current F59 still supplies immediate notification for ordinary departures',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, candidate=True, stale_sweep=True)
    b.check('UNBUILT IDEA: exact expedition-home exclusion preserves the hold with competing neighbour',
            rt.eval('crew.reserved_residence == home and home.reserved[crew] == true and homeless.residence == false'))
    rt = scenario(True, candidate=True, action='ordinary')
    b.check('UNBUILT IDEA: ordinary vacancy still offered immediately',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, candidate=True, action='unrelated_hold')
    b.check('UNBUILT IDEA: unrelated expedition pointer does not suppress this vacancy',
            rt.eval('homeless.residence == home'))
    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
