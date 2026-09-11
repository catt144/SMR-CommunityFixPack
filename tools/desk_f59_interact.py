#!/usr/bin/env python3
"""F59 verification, 2026-09-11: the hook also fires inside the MANUAL-ASSIGN
operation, and that one overfills a residence.

Re-derivation control for checklist 151 a. Astra's `desk_f59_expedition.py`
measured the expedition-boarding window. This measures a SECOND shipped caller
that reaches `Colonist:SetResidence(false)` as a MIDDLE step of a larger
operation: `Residence:ColonistInteract` -> `KickOldestResident` ->
`KickResident`. Our post-hook runs between the kick and the assignment, so a
homeless colonist (the just-kicked resident included -- `UpdateHomelessLabels`
puts them in the dome label inside the same call) can take the very slot
`ColonistInteract` is about to hand to the forced colonist. The next shipped
statement is `assert(self:GetFreeSpace() > 0)` followed by an unconditional
insert (`Residence.lua:111-112`), and by `EF-008` an assert does not unwind.

`assert` is therefore shimmed to RECORD-AND-CONTINUE, which is the engine's
retail behaviour (`EF-008`), not lupa's. Labels, comfort, UI and geometry are
fixtures. This establishes that the shipped bodies discriminate on the module
being loaded; it is NOT a colony reproduction.
"""
import deskbench as db
from desk_migration_cluster import runtime, shipped, module


def scenario(patched, alt_home=False):
    rt = runtime()
    rt.execute('''
      function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
      IsKindOf=function(o,c) return type(o)=="table" and o.kind==c end
      Msg=function() end; RebuildInfopanel=function() end
      UpdateAttachedSign=function() end
      GameTime=function() return 100 end
      min_int=-999999; GetResidenceComfort=function() return 50,0 end
      TraitPresets={}; ColonistFilterFunc={}; FilterRejectMessage={}
      T=function() return "" end
      Clamp=function(v,lo,hi) if v<lo then return lo elseif v>hi then return hi end return v end
      g_Consts.ForcedByUserLockTimeout=3600000
      -- EF-008: assert() reports and execution CONTINUES. lupa's would unwind and
      -- hide the overflow, so the engine's behaviour is modelled explicitly.
      asserts_fired={}
      assert=function(cond,msg) if not cond then asserts_fired[#asserts_fired+1]=msg or "assert" end return cond end
    ''')
    for method in ['SetResidence', 'UpdateResidence', 'CancelResidenceReservation',
                   'CanChangeCommand', 'CheckForcedResidence', 'CheckForcedDome',
                   'UpdateHomelessLabels']:
        shipped(rt, 'Lua/Units/Colonist.lua', '^function Colonist:' + method + r'\(')
    for method in ['AddResident', 'RemoveResident', 'GetFreeSpace', 'CanReserveResidence',
                   'ReserveResidence', 'CancelResidenceReservation', 'CheckHomeForHomeless',
                   'IsSuitable', 'KickResident', 'KickOldestResident', 'ColonistInteract',
                   'GetUICapacity', 'GetUIResidentsCount']:
        shipped(rt, 'Lua/Buildings/Residence.lua', '^function Residence:' + method + r'\(')
    shipped(rt, 'Lua/Buildings/Residence.lua', r'^function ChooseResidence\(')
    shipped(rt, 'Lua/Buildings/Dome.lua', r'^function Dome:ChooseResidence\(')
    rt.execute('ALT = ' + ('true' if alt_home else 'false'))
    if patched:
        module(rt, 'FreedHousingNotice')
    rt.execute('''
      local noop=function() end
      dome={working=true,ui_working=true,labels={Homeless={}},
        ResetFreeSpace=noop, ChooseResidence=Dome.ChooseResidence,
        AddToLabel=function(self,l,c) self.labels[l]=self.labels[l] or {}; table.insert_unique(self.labels[l],c) end,
        RemoveFromLabel=function(self,l,c) table.remove_entry(self.labels[l] or {},c) end}
      city={labels={Residence={}},
        AddToLabel=function(self,l,c) self.labels[l]=self.labels[l] or {}; table.insert_unique(self.labels[l],c) end,
        RemoveFromLabel=function(self,l,c) table.remove_entry(self.labels[l] or {},c) end}
      MainCity=city
      home=setmetatable({parent_dome=dome,working=true,ui_working=true,capacity=2,closed=0,
        filter_residents="Everyone",colonists={},reserved={},UpdateOccupation=noop}, {__index=Residence})
      dome.labels.Residence={home}; city.labels.Residence={home}
      local function colonist(age)
        return setmetatable({dome=dome,city=city,traits={},residence=false,reserved_residence=false,age=age,
          CanVote=function() return false end, SetWorkplace=noop, Affect=noop,
          IsDying=function() return false end, IsTransported=function() return false end,
          UpdateLowComfortNotification=noop, UpdateMorale=noop, SetForcedDome=noop,
          ClearDetrimentalStatusEffects=noop, AssignToService=noop, SetOutside=noop,
          ClearTransportRequest=Colonist.CancelResidenceReservation}, {__index=Colonist})
      end
      old=colonist(50); young=colonist(20); newcomer=colonist(30)
      home.colonists={old,young}; old.residence=home; young.residence=home
      newcomer:UpdateHomelessLabels()
      if ALT then
        -- a better-comfort free bed elsewhere in the dome: the kicked resident
        -- should prefer it, so nobody competes for the slot in hand
        alt=setmetatable({parent_dome=dome,working=true,ui_working=true,capacity=1,closed=0,
          filter_residents="Everyone",colonists={},reserved={},UpdateOccupation=noop}, {__index=Residence})
        dome.labels.Residence={home,alt}; city.labels.Residence={home,alt}
        GetResidenceComfort=function(r) if r==alt then return 90,0 end return 50,0 end
      end
      -- the player's "Set Residence" on a FULL residence
      home:ColonistInteract(newcomer)
    ''')
    return rt


def main():
    b = db.Bench('F59 manual assign: same shipped ColonistInteract, module off/on controls')

    rt = scenario(False)
    b.check('vanilla: the kicked resident is evicted and the forced colonist takes the slot',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and old.residence == false'))
    b.check('vanilla: the residence stays within capacity and no assert fires',
            rt.eval('home:GetUIResidentsCount() == 2 and home:GetUICapacity() == 2 and #asserts_fired == 0'))

    rt = scenario(True)
    b.check('F59 applied: the hook re-homes the just-kicked resident into the slot in hand',
            rt.eval('old.residence == home'))
    b.check('F59 applied: the forced colonist is inserted anyway -> OVER-CAPACITY residence',
            rt.eval('#home.colonists == 3 and home.capacity == 2 and newcomer.residence == home'))
    b.check('F59 applied: the capacity assert fired (EF-008: reported, did not unwind)',
            rt.eval('#asserts_fired == 1'))
    b.check('F59 applied: the player-visible infopanel count exceeds capacity',
            rt.eval('home:GetUIResidentsCount() == 3 and home:GetUICapacity() == 2'))

    rt = scenario(True, alt_home=True)
    b.check('negative control: a better free bed elsewhere draws the kicked resident away',
            rt.eval('old.residence ~= home and old.residence ~= false'))
    b.check('negative control: with nobody competing, the assignment stays within capacity',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and #asserts_fired == 0'))

    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
