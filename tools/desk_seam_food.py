#!/usr/bin/env python3
"""Vanillahunt 03 source controls; no game, mod, or archive writes.

Extracts archived shipped bodies with deskbench/luafn. Production collectors,
resource formatting, unmodified production bonuses and deterministic integer
rounding are explicit stand-ins. Native storage, scheduler and UI are not run.
The ingredient fixture is synthetic; it exercises the BASE implementation with
an ingredient registry present/absent, not the DLC's own preset loader.
"""
from pathlib import Path
import deskbench as d

ARCHIVE = Path(d.SRC_ARCHIVE).parent.parent
for version, folder in (("1.0.7", "1.0.7.396349"), ("1.1.0", "1.1.0.403908")):
    d.TREES[version] = str(ARCHIVE / folder / "Src")


def install(rt, rel, name, version="1.1.0"):
    text, first, _ = d.body(rel, r"^function " + name + r"\(", version)
    d.load_at(rt, text, "=" + rel, first)


def pasture(version, performance, broken=False):
    rt = d.lua_runtime()
    rt.execute("""
        Pasture = {}; Presets = {Animal = {Pasture = {}}}
        const = {ResourceScale = 1000}; g_NativeFoodProduction = 100
        empty_table = {}; Min = math.min; Max = math.max
        function MulDivRound(a,b,c) return math.floor(a*b/c + 0.5) end
        function round(a,step) return math.floor(a/step + 0.5)*step end
        function T(_,text) return text end
        function PlaceObj(class,obj) Presets.Animal.Pasture[obj.id] = obj end
        function Msg(...) end
        function ObjModified(...) end
        function IsFoodResource(res) return res == 'Food' end
        function TLookupTag(t) return t end
        function FormatResource(_,amount,res) ui_amount = amount; return tostring(amount) end
    """)
    # Load the actual base animal data instead of retyping output/herd values.
    rel = "Data/Animal.lua"
    d.load_at(rt, d.read(Path(d.TREES[version]) / rel), "=" + rel)
    rel = "Lua/Units/Animals.lua"
    for name in ("Pasture:ProduceFood", "Pasture:CalcExpectedProduction"):
        install(rt, rel, name, version)
    if version == "1.1.0":
        for name in ("Pasture:GetBreedOutputResources", "Pasture:GetPrimaryBreedOutput",
                     "Pasture:ApplyOutputModifier", "Pasture:GetUIBreedProductionText"):
            install(rt, rel, name, version)
        install(rt, "Lua/Resources.lua", "RoundResourceAmountToTenth", version)
        if broken:
            # Deliberate falsifier: removing per-animal quantization MUST kill
            # the discrepancy assertion below. This is not a proposed repair.
            rt.execute("RoundResourceAmountToTenth = function(amount) return amount end")
    rt.globals().performance = performance
    return rt.execute("""
        local info = Presets.Animal.Pasture.Chicken
        assert(info.herd_size == 25)
        produced_total = 0
        local producer = {Produce = function(self,amount)
            produced_total = produced_total + amount; return amount
        end}
        local obj = setmetatable({working=true, current_harvest_idx=1,
            current_herd={}, performance_avg=performance,
            herd_performance_sum=performance, herd_performance_calculations=1,
            max_resources_produced=3, producers={Food=producer}}, {__index=Pasture})
        obj.GetProducerObj = function() return producer end
        obj.IsResourceProductionAllowed = function() return true end
        obj.ModifyValue = function(self,amount) return amount end
        for i=1,info.herd_size do obj:ProduceFood({animal_type='Chicken'}) end
        local expected = obj:CalcExpectedProduction(1,info)
        if obj.GetUIBreedProductionText then obj:GetUIBreedProductionText(1,info) end
        return produced_total, expected, ui_amount
    """)


def ingredients(enabled, present, vegan=False):
    rt = d.lua_runtime()
    rt.execute("""
        FoodBuilding = {}; Min = math.min
        g_Consts = {eat_ingredient_per_visit = 100}
        function MealIngredientBits() return ingredient_bits end
        function VeganIngredients() return 0 end
    """)
    for method in ("IsIngredientEnabled", "SetIngredientEnabled", "GetAvailableIngredientsMask",
                   "GetIngredientConsumeGate", "ConsumeMealIngredientsMask"):
        install(rt, "Lua/Buildings/FoodServiceBuilding.lua", "FoodBuilding:" + method)
    rt.globals().enabled = enabled
    rt.globals().present = present
    rt.globals().vegan = vegan
    return rt.execute("""
        ingredient_bits = present and {FixtureIngredient=1} or {}
        local obj = setmetatable({stored_resources={FixtureIngredient=300},
            serveable_ingredients={'FixtureIngredient'}, city={}}, {__index=FoodBuilding})
        obj.GetStoredAmount = function(self,res) return self.stored_resources[res] or 0 end
        obj.DecreaseStoredInputResource = function(self,res,amount)
            self.stored_resources[res] = self.stored_resources[res] - amount
        end
        obj.UpdateRequestsSuspendState = function() end
        obj.UpdateIngredientsDemand = function() end
        obj.city.OnConsumptionResourceConsumed = function() end
        obj:SetIngredientEnabled('FixtureIngredient',enabled)
        local advertised = obj:GetAvailableIngredientsMask()
        local consumed = obj:ConsumeMealIngredientsMask({traits={Vegan=vegan}})
        return advertised, consumed, obj.stored_resources.FixtureIngredient
    """)


def next_crop(version, gap):
    rt = d.lua_runtime()
    rt.execute("""
        FarmBase = {}; CropPresets = {A={DisplayName='A'}, B={DisplayName='B'}}
        function T(_,text) return text end
        function GetCropDisplayNameWithResource(info) return info.DisplayName end
    """)
    install(rt, "Lua/Buildings/Farm.lua", "FarmBase:GetNextCrop", version)
    rt.globals().gap = gap
    return rt.execute("""
        local obj = setmetatable({current_crop=1,
            selected_crop={'A', gap and false or 'B', 'B'}}, {__index=FarmBase})
        -- Lua's and/or idiom cannot represent false in a ternary.
        if gap then obj.selected_crop[2] = false end
        return obj:GetNextCrop()
    """)


def main():
    print("SEAM DESK:", d.lua_version(), "(archived bodies; no runtime claim)")
    for version in ("1.0.7", "1.1.0"):
        for perf in (0, 48, 100):
            actual, expected, ui = pasture(version, perf)
            print(f"pasture {version} performance={perf}: actual={actual}, expected={expected}, ui={ui}")
            if perf == 48 and version == "1.1.0":
                assert (actual, expected, ui) == (2500, 1200, 1200)
            else:
                assert actual == expected
    corrected = pasture("1.1.0", 48, broken=True)
    assert corrected == (1200, 1200, 1200), corrected
    print("counterfactual identity round helper: mismatch demand would FAIL (control discriminates)")
    for enabled, present, vegan, demand in (
        (True, True, False, (1, 1, 200)),
        (False, True, False, (0, 1, 200)),
        (False, False, False, (0, 0, 300)),
        (True, True, True, (1, 0, 300)),
    ):
        result = ingredients(enabled, present, vegan)
        print(f"ingredient enabled={enabled} registry={present} vegan={vegan}: advertised, consumed, remaining={result}")
        assert result == demand, (result, demand)
    # Absence is checked by the shared delimiter; this is not an old-DLC run.
    old_path = Path(d.TREES["1.0.7"]) / "Lua/Buildings/FoodServiceBuilding.lua"
    assert not old_path.exists()
    print("1.0.7: ingredient consumer absent; no equivalent ingredient behavior control claimed")
    for version in ("1.0.7", "1.1.0"):
        assert next_crop(version, False) == "B"
        assert next_crop(version, True) == "None"
        print(f"GetNextCrop {version}: adjacent=B, gap-before-B=None (bounded loop; player caller not found)")
    print("PASS: pasture branch difference and ingredient-toggle contradiction discriminate")


if __name__ == "__main__":
    main()
