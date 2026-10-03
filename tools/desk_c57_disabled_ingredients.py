#!/usr/bin/env python3
"""C57 disabled-ingredient control on archived 1.1.1.406343 meal and storage bodies.

No engine, scheduler, DLC loader, UI or game execution. The registered Meat
fixture corresponds to DLC/norman/Presets/Resource.lua:390-407. Its registry,
300 units of residual stock and 100 per visit are explicit fixture inputs.
All eligibility, toggle, consumption and physical storage mutation bodies are
shipped. Request flag/amount setters only collect notifications; no returned
value participates in a consumption or eligibility decision. The city accounting
callback is a notification. There is no canned validity or rejecting-body stub.
A scratch consumer variant adds the missing toggle gate and must fail the
disabled-stock discrepancy demand. Files on disk are never modified by a run.
"""
from pathlib import Path

import deskbench as d

SRC = Path(r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.406343\Src")


def install(rt, rel, name, variant=False):
    d.TREES["c57-current"] = str(SRC)
    text, first, last = d.body(rel, "^function " + name + r"\(", "c57-current")
    if variant and name == "FoodBuilding:ConsumeMealIngredientsMask":
        old = "if bit and (gate & bit) ~= 0 then"
        assert text.count(old) == 1
        text = text.replace(old, "if bit and self:IsIngredientEnabled(res) and (gate & bit) ~= 0 then")
    d.load_at(rt, text, "=" + rel, first)
    return first, last


def run(enabled, vegan=False, present=True, variant=False):
    rt = d.lua_runtime()
    rt.execute(d.ENGINE_SHIMS + """
        FoodBuilding = {}; InputResourceHost = {}; ActiveLaws = {}
        g_Consts = {eat_ingredient_per_visit=100}; rfSuspended=1
        Resources = {Meat={vegan=false}}; MealIngredientIds={}
    """)
    for name in ("MealIngredientBits", "VeganIngredients"):
        install(rt, "Lua/Meal.lua", name)
    for name in ("SetStoredInputResource", "DecreaseStoredInputResource"):
        install(rt, "Lua/Buildings/RecipeProductionBuilding.lua", "InputResourceHost:" + name)
    rt.execute("setmetatable(FoodBuilding, {__index=InputResourceHost})")
    for name in ("SyncInputResourceVisual", "GetStoredAmount", "IsIngredientEnabled",
                 "UpdateRequestsSuspendState", "UpdateIngredientsDemand", "UpdateIngredientsSupply",
                 "SetIngredientEnabled", "GetAvailableIngredientsMask", "GetIngredientConsumeGate",
                 "ConsumeMealIngredientsMask"):
        install(rt, "Lua/Buildings/FoodServiceBuilding.lua", "FoodBuilding:" + name, variant)
    rt.globals().fixture_enabled = enabled
    rt.globals().fixture_vegan = vegan
    rt.globals().fixture_present = present
    return rt.execute("""
        MealIngredientIds = fixture_present and {'Meat'} or {}
        local request = {
            SetAmount=function(self, amount) self.amount=amount end,
            AddFlags=function(self, flags) self.flags=flags end,
            ClearFlags=function(self, flags) self.flags=0 end,
        }
        local b = setmetatable({stored_resources={Meat=300}, serveable_ingredients={'Meat'},
            ingredient_demand_requests={Meat=request}, ingredient_supply_requests={Meat=request},
            food_demand_requests={}, food_stockpile_controller=false, ui_working=true,
            DemandPerIngredient=1000, city={OnConsumptionResourceConsumed=function() end}},
            {__index=FoodBuilding})
        -- Enabled path removes its existing supply request; these calls are notifications.
        b.InterruptDrones=function() end
        b.RemoveRequest=function() end
        b:SetIngredientEnabled('Meat', fixture_enabled)
        local mask=b:GetAvailableIngredientsMask()
        local consumed=b:ConsumeMealIngredientsMask({traits={Vegan=fixture_vegan}})
        return mask, consumed, b:GetStoredAmount('Meat')
    """)


def defect_demand(variant=False):
    result = run(False, variant=variant)
    assert result == (0, 1, 200), result
    return result


def main():
    print("C57 build 25579348 / 1.1.1.406343:", d.lua_version())
    print("disabled advertised/consumed/remaining:", defect_demand())
    for enabled, vegan, present, expected in (
        (True, False, True, (1, 1, 200)),
        (False, True, True, (0, 0, 300)),
        (False, False, False, (0, 0, 300)),
    ):
        actual = run(enabled, vegan, present)
        assert actual == expected, actual
        print("control enabled/vegan/registry", enabled, vegan, present, actual)
    try:
        defect_demand(variant=True)
    except AssertionError as e:
        print("falsifying toggle-gate variant: demand FAILS", e)
    else:
        raise AssertionError("falsifying variant passed defect demand")
    print("PASS: toggle contradiction controlled; gameplay reach and hauling not executed")


if __name__ == "__main__":
    main()
