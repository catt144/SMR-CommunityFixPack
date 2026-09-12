#!/usr/bin/env python3
"""F59: immediate vacancy notification can steal an expedition home, and the
repair (2026-09-11) defers the notification out of the caller's call stack.

Runs extracted Colonist.EnterTransporter -> SetDome -> SetResidence, followed by
extracted OnDisappear, with real residence selection/reservation bodies and whole
F59/F58 modules. Unit.EnterTransporter is a named engine-boundary stub: it marks
disappeared and calls OnDisappear (the real path goes via Unit.Disappear).
Labels, UI, comfort, geometry and trait-free suitability are fixtures. No claim
about engine timing, real expedition completion, or in-play reproduction.

THREE MODULE SHAPES are compared, which is what makes this a falsifier rather
than a demonstration:
  * absent           -- vanilla ordering.
  * `legacy=True`    -- the PRE-REPAIR wrapper, extracted from git at
                        desk_migration_cluster.F59_HARMFUL_REV. The harm legs run
                        on this, because the repair deleted the harmful shape
                        from Code/ and a leg that can no longer express the harm
                        is not evidence that the harm was ever there.
  * shipped          -- today's Code/ module, which must NOT express it.
And `synchronous=True` defeats the deferral on the SHIPPED module: under it the
harm must come back. That is the control proving the repair is the deferral and
not some incidental change to the guard.
"""
import deskbench as db
from desk_migration_cluster import (runtime, shipped, module, module_text,
                                    load_module, defer_shim, F59_HARMFUL_REV)


def scenario(patched, waiting=True, stale_sweep=False, action='expedition',
             candidate=False, legacy=False, synchronous=False, real_comfort=False):
    rt = runtime()
    defer_shim(rt, synchronous)
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
            # THE AUDIT'S UNBUILT IDEA, kept as a record of what it did and did
            # not buy. It is a transform of the PRE-REPAIR body (the shape it was
            # proposed against), in memory, never of a Code file: capture the
            # exact departing expedition home before orig can mutate it.
            # ⛔ It covers A1 only. desk_f59_interact.py runs the same transform
            # against A2 and the overfill still happens -- which is why the
            # shipped repair is not this.
            text, _ = module_text('FreedHousingNotice', F59_HARMFUL_REV)
            needle = 'local left = self.residence'
            assert text.count(needle) == 1
            text = text.replace(needle, needle + '\n\t\t\tlocal expedition_home = left and self.expedition_residence == left')
            needle = 'if left and left ~= self.residence and IsValid(left)'
            assert text.count(needle) == 1
            text = text.replace(needle, 'if not expedition_home and left and left ~= self.residence and IsValid(left)')
            load_module(rt, 'FreedHousingNotice', text, 'F59_UNBUILT_IDEA')
        else:
            module(rt, 'FreedHousingNotice', F59_HARMFUL_REV if legacy else None)
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
    if real_comfort:
        # ⛔ The constant-comfort stub silently removes a VANILLA GUARD: the real
        # `GetResidenceComfort` (Residence.lua:416-434) gates on `ValidateBuilding`
        # (Workplace.lua:1316-1327), which tests destroyed/demolishing/refab.
        # A1 involves no destroyed building, so this must change nothing here --
        # which is exactly why it is worth running.
        shipped(rt, 'Lua/Buildings/Workplace.lua', r'^function ValidateBuilding\(')
        shipped(rt, 'Lua/Buildings/Residence.lua', r'^function GetResidenceComfort\(')
        rt.execute('ColonistStatList = {"Comfort"}')
        rt.execute('home.Comfort = 50')
        rt.execute('home.IsKindOf = function() return false end')
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
    # the next scheduler opportunity, AFTER the shipped operation returned
    rt.execute('DEFERRED_RAN = RunDeferred()')
    return rt


def main():
    b = db.Bench('F59 expedition hold: same shipped sequence, module absent / pre-repair / repaired')

    rt = scenario(False)
    b.check('vanilla: crew retains reserved home with a homeless neighbour',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home and home.reserved[crew] == true and homeless.residence == false'))

    # --- the measured harm, on the shape that shipped it (extracted from git) ---
    rt = scenario(True, legacy=True)
    b.check('PRE-REPAIR: neighbour takes bed and expedition hold is lost',
            rt.eval('homeless.residence == home and crew.expedition_residence == false and crew.reserved_residence == false and not home.reserved[crew]'))
    b.check('PRE-REPAIR: residence remains within capacity (this is loss of hold, not overflow)',
            rt.eval('#home.colonists == 1 and #home.reserved == 0'))

    # --- the repair ---
    rt = scenario(True)
    b.check('REPAIRED: the expedition hold survives a competing homeless neighbour',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home and home.reserved[crew] == true'))
    b.check('REPAIRED: the neighbour is not given a bed the boarding crew still holds',
            rt.eval('homeless.residence == false and #home.colonists == 0 and #home.reserved == 1'))
    b.check('REPAIRED: the deferred notification really ran (it declined, it was not skipped)',
            rt.eval('DEFERRED_RAN == 1'))

    # --- the falsifier for the repair itself: defeat the deferral, harm returns ---
    rt = scenario(True, synchronous=True)
    b.check('CONTROL: with the deferral defeated the harm returns => the deferral IS the repair',
            rt.eval('homeless.residence == home and crew.reserved_residence == false'))

    rt = scenario(True, waiting=False)
    b.check('negative control: REPAIRED preserves crew home when no neighbour competes',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home'))

    rt = scenario(True, stale_sweep=True, legacy=True)
    b.check('PRE-REPAIR: F58 exemption cannot protect a hold F59 prevented from being created',
            rt.eval('homeless.residence == home and crew.expedition_residence == false and crew.reserved_residence == false'))
    rt.execute('OnMsg.NewDay()')
    b.check('PRE-REPAIR: F58 daily sweep does not restore the missing hold',
            rt.eval('homeless.residence == home and crew.reserved_residence == false'))
    rt = scenario(True, stale_sweep=True)
    b.check('REPAIRED: with F58 also loaded the hold is held, so F58 has nothing to rescue',
            rt.eval('crew.reserved_residence == home and home.reserved[crew] == true'))

    # --- the benefit the module exists for, which the repair must not lose ---
    rt = scenario(False, action='ordinary')
    b.check('original F59 gap: vanilla ordinary departure leaves an eligible neighbour homeless beside a free bed',
            rt.eval('home:GetFreeSpace() == 1 and homeless.residence == false'))
    rt.execute('homeless:UpdateResidence()')
    b.check('original-gap control: a later housing update takes that same bed',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, legacy=True, action='ordinary')
    b.check('PRE-REPAIR: ordinary departure was notified immediately',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, action='ordinary')
    b.check('REPAIRED: ordinary departure is STILL notified, one scheduler step later',
            rt.eval('homeless.residence == home and DEFERRED_RAN >= 1'))

    # --- the audit's unbuilt candidate: what it bought, recorded, not shipped ---
    rt = scenario(True, candidate=True, stale_sweep=True)
    b.check('AUDIT IDEA (A1 only): exact expedition-home exclusion preserves the hold',
            rt.eval('crew.reserved_residence == home and home.reserved[crew] == true and homeless.residence == false'))
    rt = scenario(True, candidate=True, action='ordinary')
    b.check('AUDIT IDEA: ordinary vacancy still offered immediately',
            rt.eval('homeless.residence == home'))
    rt = scenario(True, candidate=True, action='unrelated_hold')
    b.check('AUDIT IDEA: unrelated expedition pointer does not suppress this vacancy',
            rt.eval('homeless.residence == home'))
    # --- the same legs without the comfort STUB. A3 (a third harm I reported at
    # Residence:OnDestroyed while building) turned out to be an artefact of a
    # constant-comfort stub, which silently deletes the `destroyed` test the real
    # `GetResidenceComfort` inherits from `ValidateBuilding` (Workplace.lua:1322).
    # A1 involves no destroyed building so nothing here should move -- and that is
    # precisely why it is asserted rather than assumed. See desk_f59_interact.py.
    rt = scenario(True, legacy=True, real_comfort=True)
    b.check('REAL comfort: the A1 hold loss is REAL -- neighbour takes the bed, hold cleared',
            rt.eval('homeless.residence == home and crew.reserved_residence == false'))
    rt = scenario(True, real_comfort=True)
    b.check('REAL comfort: REPAIRED keeps the expedition hold against a competing neighbour',
            rt.eval('crew.expedition_residence == home and crew.reserved_residence == home and home.reserved[crew] == true and homeless.residence == false'))
    rt = scenario(True, synchronous=True, real_comfort=True)
    b.check('REAL comfort: defeating the deferral loses the hold again',
            rt.eval('crew.reserved_residence == false and homeless.residence == home'))
    rt = scenario(True, action='ordinary', real_comfort=True)
    b.check('REAL comfort: an ordinary vacancy is still offered (the benefit survives)',
            rt.eval('homeless.residence == home and DEFERRED_RAN >= 1'))
    rt = scenario(False, action='ordinary', real_comfort=True)
    b.check('REAL comfort: vanilla still leaves that neighbour homeless beside the free bed',
            rt.eval('homeless.residence == false and home:GetFreeSpace() == 1'))

    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
