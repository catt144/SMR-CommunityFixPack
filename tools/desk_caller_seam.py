#!/usr/bin/env python3
"""Vanillahunt 03d source control; no game, mod, or archive writes.

Executes the shipped SA_WaitResearch:SAExec bodies with explicit research and
WaitMsg shims. This proves the branch distinction only; scheduler and mystery
runtime behaviour remain unmeasured.
"""
from pathlib import Path

import deskbench as d


ARCHIVE = Path(d.SRC_ARCHIVE).parent.parent
for version, folder in (("1.0.7", "1.0.7.396349"), ("1.1.0", "1.1.0.403908")):
    d.TREES[version] = str(ARCHIVE / folder / "Src")


def run(version, researched, active):
    rt = d.lua_runtime()
    rt.execute("""
        SA_WaitResearch = {}
        waits = {}
        researched = fixture_researched
        active = fixture_active
        UIColony = {}
        function UIColony:IsTechDiscovered(_) return true end
        function UIColony:IsTechUnlocked(_) return true end
        function UIColony:IsTechResearched(_) return researched end
        function UIColony:GetResearchInfo() return active and 'NumberSixTracing' or false end
        function WaitMsg(name)
            waits[#waits + 1] = name
            -- Let a mistaken wait finish without faking its first observation.
            researched = true
        end
    """)
    rt.globals().fixture_researched = researched
    rt.globals().fixture_active = active
    # Globals assigned after the table chunk above need copying explicitly.
    rt.execute("researched = fixture_researched; active = fixture_active")
    text, first, _ = d.body(
        "Lua/Sequences/SA_Gameplay.lua",
        r"^function SA_WaitResearch:SAExec\(",
        version,
    )
    d.load_at(rt, text, "=Lua/Sequences/SA_Gameplay.lua", first)
    return rt.execute("""
        local obj = setmetatable({Research='NumberSixTracing',
            State='In Progress'}, {__index=SA_WaitResearch})
        obj:SAExec()
        return #waits, waits[1]
    """)


def shift_return(same_shift):
    rt = d.lua_runtime()
    rt.execute("""
        FoodServiceBuilding = {}; FoodBuilding = {}; ServiceWorkplace = {}
        Max = math.max
        function ServiceWorkplace.OnChangeWorkshift(...) end
        function FoodBuilding.ReturnMealPortion(self, colonist)
            colonist.meal_assigned_amount = 0
        end
    """)
    for name in ("OnChangeWorkshift", "ReturnMealPortion"):
        text, first, _ = d.body(
            "Lua/Buildings/FoodServiceBuilding.lua",
            r"^function FoodServiceBuilding:" + name + r"\(",
            "1.1.0",
        )
        d.load_at(rt, text, "=Lua/Buildings/FoodServiceBuilding.lua", first)
    rt.globals().same_shift = same_shift
    return rt.execute("""
        local service = setmetatable({meals_this_shift=1}, {__index=FoodServiceBuilding})
        local old_reservation = {meal_assigned_amount=1000}
        if same_shift then
            -- A and B are both in this shift.
            service.meals_this_shift = 2
        else
            -- A survives the rollover; B is the first reservation of the new shift.
            service:OnChangeWorkshift(1, 2)
            service.meals_this_shift = service.meals_this_shift + 1
        end
        service:ReturnMealPortion(old_reservation)
        return service.meals_this_shift
    """)


def visit(entered):
    rt = d.lua_runtime()
    rt.execute("""
        Colonist = {}; ServiceFailure = {NotFound=1, Full=2}; ActiveLaws = {}
        const = {Scale={Stat=1}}; TraitPresets = {}; stat_scale = 1
        function IsValid(_) return true end
        function IsUnitInDome(_) return false end
        function RecordServiceFail(...) end
        function find(...) return false end
        function GameTime() return 10 end
        function Sleep(...) end
        function IsKindOf(...) return false end
    """)
    text, first, _ = d.body(
        "Lua/Units/Colonist.lua", r"^function Colonist:VisitService\(", "1.1.0"
    )
    d.load_at(rt, text, "=Lua/Units/Colonist.lua", first)
    rt.globals().fixture_entered = entered
    return rt.execute("""
        local service = {
            visitors={}, fulfilled=0,
            HasFreeVisitSlots=function() return true end,
            Service=function() end,
            FulfillMealPortion=function(self) self.fulfilled=self.fulfilled+1 end,
            ConsumeMealIngredientsMask=function() return 0 end,
            OnFoodEaten=function() end,
        }
        local obj = setmetatable({meal_amount=1000, meal_from_pile=false,
            traits={}, daily_interest='', destructors={}}, {__index=Colonist})
        obj.PushDestructor=function(self, fn) self.destructors[#self.destructors+1]=fn; return #self.destructors end
        obj.PopAndCallDestructor=function() end
        obj.PopDestructor=function() end
        obj.ClearMealState=function(self) self.meal_amount=0 end
        obj.AssignToService=function() end
        obj.EnterBuilding=function() return fixture_entered end
        obj.Eat=function(self, amount) self.eaten=(self.eaten or 0)+amount end
        obj.ApplyIngredientStats=function() end
        obj.SetState=function() end
        obj:VisitService(service, 'needFood')
        return service.fulfilled, obj.eaten or 0
    """)


def main():
    print("CALLER SEAM DESK:", d.lua_version(), "(archived bodies; no runtime claim)")
    old_active = run("1.0.7", False, True)
    new_active = run("1.1.0", False, True)
    old_done = run("1.0.7", True, False)
    new_done = run("1.1.0", True, False)
    print("In Progress while active, 1.0.7 waits:", old_active)
    print("In Progress while active, 1.1.0 waits:", new_active)
    print("already researched control, 1.0.7/1.1.0:", old_done, new_done)
    assert old_active == (0, None)
    assert new_active == (1, "TechResearched")
    assert old_done == new_done == (0, None)
    print("counterfactual: restoring the named In Progress branch makes the active case return without a wait")
    same_shift = shift_return(True)
    across_shift = shift_return(False)
    print("meal return, same-shift A+B remaining count:", same_shift)
    print("meal return, old A/new-shift B remaining count:", across_shift)
    assert same_shift == 1
    assert across_shift == 0
    print("counterfactual: tagging A with its reservation shift would leave new-shift B counted")
    arrived = visit(True)
    failed = visit(False)
    print("VisitService entered=true fulfilled/eaten:", arrived)
    print("VisitService entered=false fulfilled/eaten:", failed)
    assert arrived == failed == (1, 1000)
    print("counterfactual: guarding fulfillment/eating with successful entry would make the false case (0, 0)")
    print("PROBE SWEEP: clean")
    print("PASS: all three seam contradictions discriminate")


if __name__ == "__main__":
    main()
