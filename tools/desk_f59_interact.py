#!/usr/bin/env python3
"""F59 verification, 2026-09-11: the hook also fires inside the MANUAL-ASSIGN
operation, and that one overfilled a residence -- plus the repair that stops it.

Re-derivation control for checklist 151 a. Astra's `desk_f59_expedition.py`
measured the expedition-boarding window. This measures a SECOND shipped caller
that reaches `Colonist:SetResidence(false)` as a MIDDLE step of a larger
operation: `Residence:ColonistInteract` -> `KickOldestResident` ->
`KickResident`. The pre-repair post-hook ran between the kick and the
assignment, so a homeless colonist (the just-kicked resident included --
`UpdateHomelessLabels` puts them in the dome label inside the same call) could
take the very slot `ColonistInteract` was about to hand to the forced colonist.
The next shipped statement is `assert(self:GetFreeSpace() > 0)` followed by an
unconditional insert (`Residence.lua:111-112`), and by `EF-008` an assert does
not unwind.

`assert` is therefore shimmed to RECORD-AND-CONTINUE, which is the engine's
retail behaviour (`EF-008`), not lupa's. Labels, comfort, UI and geometry are
fixtures. This establishes that the shipped bodies discriminate on the module
being loaded; it is NOT a colony reproduction.

MODULE SHAPES, as in the expedition harness: absent / `legacy=True` (the
PRE-REPAIR wrapper, extracted from git at `F59_HARMFUL_REV`, which is what the
overfill legs run on) / shipped. `synchronous=True` defeats the repair's
deferral and the overfill must return. `candidate=True` runs the migration
audit's PROPOSED expedition-home exclusion against THIS harm, and it still
overfills -- the measured reason the shipped repair is not that shape.
"""
import deskbench as db
from desk_migration_cluster import (runtime, shipped as M_shipped, module, module_text,
                                    load_module, defer_shim, F59_HARMFUL_REV)


def scenario(patched, alt_home=False, legacy=False, synchronous=False,
             candidate=False, action='interact', capacity=2, real_comfort=False):
    rt = runtime()
    defer_shim(rt, synchronous)
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
        M_shipped(rt, 'Lua/Units/Colonist.lua', '^function Colonist:' + method + r'\(')
    for method in ['AddResident', 'RemoveResident', 'GetFreeSpace', 'CanReserveResidence',
                   'ReserveResidence', 'CancelResidenceReservation', 'CheckHomeForHomeless',
                   'IsSuitable', 'KickResident', 'KickOldestResident', 'ColonistInteract',
                   'GetUICapacity', 'GetUIResidentsCount', 'OnDestroyed']:
        M_shipped(rt, 'Lua/Buildings/Residence.lua', '^function Residence:' + method + r'\(')
    M_shipped(rt, 'Lua/Buildings/Residence.lua', r'^function ChooseResidence\(')
    M_shipped(rt, 'Lua/Buildings/Dome.lua', r'^function Dome:ChooseResidence\(')
    rt.execute('ALT = ' + ('true' if alt_home else 'false'))
    rt.execute('CAPACITY = %d' % capacity)
    if patched:
        if candidate:
            # The migration audit's PROPOSED fix, transformed in memory over the
            # pre-repair body it was proposed against. Kept here to show what it
            # does to A2: nothing. See desk_f59_expedition.py for the A1 half.
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
      home.capacity=CAPACITY
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
    ''')
    if real_comfort:
        # ⛔ THE COMFORT STUB WAS HIDING A VANILLA GUARD. `GetResidenceComfort`
        # (Residence.lua:416-434) gates on `ValidateBuilding`
        # (Workplace.lua:1316-1327), which tests `destroyed`/`demolishing`/
        # `refab_work_request`/`exceptional_circumstances` -- so for a destroyed
        # residence the real body returns NIL, ChooseResidence scores it
        # `min_int` (:454-455) and its tie-break at :459 requires
        # `best_home ~= current_home`, which is false for a homeless colonist.
        # A constant-comfort stub removes all of that. Load the shipped bodies.
        M_shipped(rt, 'Lua/Buildings/Workplace.lua', r'^function ValidateBuilding\(')
        M_shipped(rt, 'Lua/Buildings/Residence.lua', r'^function GetResidenceComfort\(')
        rt.execute('ColonistStatList = {"Comfort"}')
        rt.execute('home.Comfort = 50; if ALT and alt then alt.Comfort = 90 end')
        # the real body reaches `residence:IsKindOf("HotelBase")` at :430
        rt.execute('home.IsKindOf = function() return false end')
        rt.execute('if ALT and alt then alt.IsKindOf = function() return false end end')
    if action == 'interact':
        # the player's "Set Residence" on a FULL residence
        rt.execute('home:ColonistInteract(newcomer)')
    elif action == 'uikick':
        # the infopanel occupant list's own kick button -- the THIRD shipped
        # caller of KickResident (Lua/XDef/sectionOccupantList.generated.lua:34,
        # sectionResidenceList.generated.lua:34). It does NOT close the slot
        # (:36 is a different branch), so the bed genuinely frees and the
        # notification is the benefit, not a harm.
        rt.execute('home:KickResident(old)')
    elif action == 'destroy':
        # `Building:Destroy` sets self.destroyed (Building.lua:1560) BEFORE
        # calling OnDestroyed (:1576); that ordering is the whole reason the
        # repair's `not destroyed` guard can see it. Residence:OnDestroyed:85
        # evicts one resident at a time and :86 is VANILLA'S OWN
        # colonist:UpdateResidence() -- which has the same exposure to being
        # re-assigned into the dying home. This leg separates the two.
        rt.execute('home.destroyed = true; home:OnDestroyed()')
    else:
        raise ValueError(action)
    # the next scheduler opportunity, AFTER the shipped operation returned
    rt.execute('DEFERRED_RAN = RunDeferred()')
    return rt


def main():
    b = db.Bench('F59 manual assign: same shipped ColonistInteract, module absent / pre-repair / repaired')

    rt = scenario(False)
    b.check('vanilla: the kicked resident is evicted and the forced colonist takes the slot',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and old.residence == false'))
    b.check('vanilla: the residence stays within capacity and no assert fires',
            rt.eval('home:GetUIResidentsCount() == 2 and home:GetUICapacity() == 2 and #asserts_fired == 0'))

    # --- the measured harm, on the shape that shipped it (extracted from git) ---
    rt = scenario(True, legacy=True)
    b.check('PRE-REPAIR: the hook re-homes the just-kicked resident into the slot in hand',
            rt.eval('old.residence == home'))
    b.check('PRE-REPAIR: the forced colonist is inserted anyway -> OVER-CAPACITY residence',
            rt.eval('#home.colonists == 3 and home.capacity == 2 and newcomer.residence == home'))
    b.check('PRE-REPAIR: the capacity assert fired (EF-008: reported, did not unwind)',
            rt.eval('#asserts_fired == 1'))
    b.check('PRE-REPAIR: the player-visible infopanel count exceeds capacity',
            rt.eval('home:GetUIResidentsCount() == 3 and home:GetUICapacity() == 2'))

    # --- the repair: this is the owner's four-click receipt, at the desk ---
    rt = scenario(True)
    b.check('REPAIRED: exactly one colonist lands and the residence stays within capacity',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and home.capacity == 2'))
    b.check("REPAIRED: the player's eviction stands -- the kicked resident is homeless",
            rt.eval('old.residence == false'))
    b.check('REPAIRED: no capacity assert fires and the infopanel reads 2/2',
            rt.eval('#asserts_fired == 0 and home:GetUIResidentsCount() == 2 and home:GetUICapacity() == 2'))
    b.check('REPAIRED: the deferred notification really ran (it declined, it was not skipped)',
            rt.eval('DEFERRED_RAN == 1'))

    # --- the falsifier for the repair itself: defeat the deferral, harm returns ---
    rt = scenario(True, synchronous=True)
    b.check('CONTROL: with the deferral defeated the overfill returns => the deferral IS the repair',
            rt.eval('#home.colonists == 3 and #asserts_fired == 1'))

    # --- the migration audit's proposed shape, measured against THIS harm ---
    rt = scenario(True, candidate=True)
    b.check('AUDIT IDEA IS INSUFFICIENT: the expedition-home exclusion still overfills on manual assign',
            rt.eval('#home.colonists == 3 and home.capacity == 2 and #asserts_fired == 1'))

    # --- negative controls ---
    rt = scenario(True, legacy=True, alt_home=True)
    b.check('negative control (pre-repair): a better free bed elsewhere draws the kicked resident away',
            rt.eval('old.residence ~= home and old.residence ~= false'))
    b.check('negative control (pre-repair): with nobody competing, the assignment stays within capacity',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and #asserts_fired == 0'))
    rt = scenario(True, alt_home=True)
    b.check('REPAIRED: with a better bed elsewhere the assignment is still exactly in capacity',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and #asserts_fired == 0'))

    # --- the benefit on KickResident's OTHER caller, which must NOT be suppressed ---
    rt = scenario(False, action='uikick')
    b.check('vanilla: the infopanel kick leaves the freed bed unoffered',
            rt.eval('#home.colonists == 1 and home:GetFreeSpace() == 1'))
    rt = scenario(True, action='uikick')
    b.check('REPAIRED: the infopanel kick DOES still offer the freed bed (same method, benign caller)',
            rt.eval('#home.colonists == 2 and home.capacity == 2 and #asserts_fired == 0 and DEFERRED_RAN == 1'))

    # --- ⛔ A3 RETRACTED. Read this before trusting any OnDestroyed claim here.
    # While building the repair I reported a third harm at Residence:OnDestroyed:
    # with one spare slot, the pre-repair hook appeared to drag a colonist who was
    # never a resident into the residence being destroyed. THAT WAS A FIXTURE
    # ARTEFACT OF THIS FILE. The fixture stubs `GetResidenceComfort` to a constant,
    # and the REAL body (Residence.lua:416-434) gates on `ValidateBuilding`
    # (Workplace.lua:1316-1327) which tests `destroyed` -- so it returns NIL for a
    # destroyed residence, `ChooseResidence` scores it `min_int` (:454-455), and the
    # only tie-break that could still pick it (:459) requires
    # `best_home ~= current_home`, false for a homeless colonist. Vanilla cannot
    # assign anyone into a destroyed residence, and neither could our old hook.
    # The legs below pin BOTH halves, because the stub-vs-real difference is the
    # whole lesson: a constant-comfort stub silently deletes a vanilla guard.
    rt = scenario(True, legacy=True, action='destroy', capacity=3)
    b.check('STUB comfort: the pre-repair hook APPEARS to drag a non-resident into a dying home',
            rt.eval('newcomer.residence == home'))
    rt = scenario(True, legacy=True, action='destroy', capacity=3, real_comfort=True)
    b.check('⛔ REAL comfort REFUTES it: the pre-repair hook drags nobody in -- A3 does not exist',
            rt.eval('newcomer.residence == false'))
    absent = scenario(False, action='destroy', capacity=3, real_comfort=True)
    repaired = scenario(True, action='destroy', capacity=3, real_comfort=True)
    probe = ('tostring(old.residence == home) .. tostring(young.residence == home) .. '
             'tostring(newcomer.residence == home)')
    b.check('REAL comfort: absent / pre-repair / repaired are INDISTINGUISHABLE at OnDestroyed',
            absent.eval(probe) == repaired.eval(probe) == 'falsefalsefalse')
    b.check("LEAD CLOSED in vanilla's favour: even vanilla's own :86 re-homes nobody into the dying home",
            absent.eval('old.residence == false and young.residence == false'))
    b.check('the repaired guard still declines at the door, so no thread is created either way',
            repaired.eval('DEFERRED_RAN == 0'))

    # --- the same real bodies against the harms that DID survive. These are the
    # legs that matter: A1/A2 were measured under the comfort stub too, so they
    # have to be re-run without it or they carry the same doubt A3 turned out to.
    rt = scenario(True, legacy=True, real_comfort=True)
    b.check('REAL comfort: A2 overfill is REAL -- 3 residents in a capacity-2 home, one assert',
            rt.eval('#home.colonists == 3 and home.capacity == 2 and #asserts_fired == 1'))
    rt = scenario(True, real_comfort=True)
    b.check('REAL comfort: REPAIRED lands exactly one colonist, 2/2, no assert',
            rt.eval('#home.colonists == 2 and newcomer.residence == home and old.residence == false and #asserts_fired == 0'))
    rt = scenario(True, synchronous=True, real_comfort=True)
    b.check('REAL comfort: defeating the deferral brings the overfill back',
            rt.eval('#home.colonists == 3 and #asserts_fired == 1'))
    rt = scenario(True, candidate=True, real_comfort=True)
    b.check("REAL comfort: the audit's expedition-only exclusion still overfills",
            rt.eval('#home.colonists == 3 and #asserts_fired == 1'))
    rt = scenario(True, action='uikick', real_comfort=True)
    b.check('REAL comfort: the infopanel kick still gets its freed bed offered',
            rt.eval('#home.colonists == 2 and #asserts_fired == 0 and DEFERRED_RAN == 1'))

    return b.finish()


if __name__ == '__main__':
    raise SystemExit(main())
