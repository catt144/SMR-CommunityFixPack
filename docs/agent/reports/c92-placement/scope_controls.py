"""C92 report evidence: offline shipped-body production/removal controls.

No mod, game, save file, account, or provider is loaded. Model fixtures are
explicit below. All production/label/modifier decision bodies come from Src.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))
import deskbench as db


def main():
    print("COMMAND python docs/agent/reports/c92-placement/scope_controls.py")
    print("HEAD " + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip())
    manifest = Path("A:/SteamLibrary/steamapps/appmanifest_3215050.acf").read_text()
    print("INSTALL app3215050 buildid=" + re.search(r'"buildid"\s+"(\d+)"', manifest)[1])
    print("SRC " + str(db.SRC_LIVE) + " baseline 1.1.0.403908")
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS + r'''
        Modifiable = {}; LabelContainer = {}; Effect_ModifyLabel = {}
        WaterExtractorBase = {}; SingleResourceProducer = {}; ResearchQueue = {}
        Modifier = {new = function(self, value) return value end}
        const = {DayDuration = 100}; UIPlayer = {tech_researched = {}}
        function MulDivRound(a,b,c) return math.floor(a*b/c + 0.5) end
        function Clamp(v, lo, hi) return math.max(lo, math.min(v,hi)) end
        function DirectlyModifiedConstValue() return nil end -- no constant override fixture
        function HasModifiablePropScale(prop) return prop == "water_production" end
        function GetModifiablePropScale(prop) return 1000 end
        function IsKindOf() return false end -- only suppresses optional display id
        function ObjectIsInEnvironment(obj, env) return obj.environment == env end
        function string.ends_with(s, suffix) return s:sub(-#suffix) == suffix end
        function table.remove_entry(t, value)
            for i=#t,1,-1 do if t[i]==value then table.remove(t,i) end end
        end
        function UpdateModWithoutCheck(obj, ...) return obj:UpdateModifier(...) end
        function UpdateModWithCheck(obj, action, mod, ...)
            if obj[mod.prop] ~= nil then return obj:UpdateModifier(action, mod, ...) end
        end
        min_int64 = -(2^63); max_int64 = 2^63-1
        Techs = {UndergroundExploitation = {
            GetParameterValue = function(self, name)
                assert(name == "production_change_percent"); return 20
            end}}
    ''')
    bodies = [
        ("Lua/Buildings/BuildingComponents.lua", r"^function SingleResourceProducer:CalcProductionAmount\("),
        ("Lua/Buildings/WaterExtractor.lua", r"^function WaterExtractorBase:OnModifiableValueChanged\("),
        ("Lua/Buildings/WaterExtractor.lua", r"^function WaterExtractorBase:ProduceSupply\("),
        ("Lua/Modifiers.lua", r"^function Modifiable:UpdateModifier\("),
        ("Lua/Modifiers.lua", r"^function Modifiable:ModifyValue\("),
        ("Lua/LabelContainer.lua", r"^function LabelContainer:SetLabelModifier\("),
        ("Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:GetLabelModifierId\("),
        ("Lua/MarsGameEffects.lua", r"^function Effect_ModifyLabel:OnApplyEffect\("),
        ("CommonLua/Libs/Research/Research.lua", r"^function ResearchQueue:IsTechResearched\("),
    ]
    for rel, pattern in bodies:
        source, lo, hi = db.body(rel, pattern)
        db.load_at(rt, source, "=" + rel, lo)
        print(f"SOURCE {rel}:{lo}-{hi} sha256={hashlib.sha256(source.encode()).hexdigest()}")
    rt.execute(r'''
        UIColony = setmetatable({labels = {}, label_modifiers = {}}, {__index=LabelContainer})
        function UIColony:IsTechResearched(id) return ResearchQueue.IsTechResearched(UIPlayer,id) end
        function UIColony:IsInLabel(label, obj) return label == "Extractors" and obj.extractor end
        water = setmetatable({base_water_production=5000, water_production=5000,
            working=true, nearby_deposits={{grade="Average"}}}, {__index=Modifiable})
        water.OnModifiableValueChanged=WaterExtractorBase.OnModifiableValueChanged
        function water:HasMember(prop) return self[prop] ~= nil end
        function water:GetPropertyMetadata() return {} end
        water.water={SetProduction=function(self, amount) self.production=amount end, production=5000}
        function water:DoesHaveUpgradeConsumption() return false end -- unupgraded fixture
        function water:ExtractResource(amount) self.extracted=amount; return amount end -- abundant deposit
        function water:ProduceWasteRock(amount) self.waste_input=amount; return false end -- unblocked
        UIColony.labels.UndergroundWaterExtractor={water}
        effect=setmetatable({Label="UndergroundWaterExtractor", Prop="water_production",
            Percent=20, Amount=0, Reason="", Stackable=false}, {__index=Effect_ModifyLabel})
        parent={city=UIColony,extractor=true}
        producer=setmetatable({production_per_day=5000,parent=parent,environment="Underground"},
            {__index=SingleResourceProducer})
        original_tech=Techs.UndergroundExploitation
    ''')
    count = 0

    def check(name, expr):
        nonlocal count
        assert rt.eval(expr), name
        count += 1
        print("PASS " + name)

    check("unresearched underground stockpile component yields 5000", "producer:CalcProductionAmount(100)==5000")
    rt.execute('UIPlayer.tech_researched.UndergroundExploitation=true; effect:OnApplyEffect(UIColony,original_tech)')
    check("researched underground stockpile component yields 6000", "producer:CalcProductionAmount(100)==6000")
    check("water modifier yields 6000, not 7200", "water.water_production==6000 and water.water.production==6000")
    rt.execute('WaterExtractorBase.ProduceSupply(water,"water",6000)')
    check("water supply extracts 6000, no second multiplier", "water.extracted==6000 and water.waste_input==6000")
    rt.execute('effect:OnApplyEffect(UIColony,original_tech)')
    check("same effect applied twice replaces modifier", "water.water_production==6000 and #water.modifications.water_production==1")
    rt.execute('producer.environment="Surface"')
    check("surface stockpile component unchanged", "producer:CalcProductionAmount(100)==5000")
    rt.execute('producer.environment="Underground"; parent.extractor=false')
    check("underground non-extractor component unchanged", "producer:CalcProductionAmount(100)==5000")
    rt.execute('parent.extractor=true; original_tech.Obsolete=true')
    check("obsolete preset retained: stockpile bonus still runs", "producer:CalcProductionAmount(100)==6000")
    check("obsolete preset retained: existing water modifier still runs", "water.water_production==6000")
    rt.execute('Techs.UndergroundExploitation=nil')
    result = rt.eval('function() return pcall(producer.CalcProductionAmount, producer, 100) end')()
    assert result[0] is False and "UndergroundExploitation" in str(result[1]), result
    count += 1
    print("PASS absent preset + researched flag triggers Lua error: " + str(result[1]))
    rt.execute('UIPlayer.tech_researched.UndergroundExploitation=nil')
    check("absent preset + cleared flag short-circuits safely", "producer:CalcProductionAmount(100)==5000")
    check("clearing flag alone leaves water modifier", "water.water_production==6000")
    rt.execute('UIColony:SetLabelModifier("UndergroundWaterExtractor",effect,nil)')
    check("normal modifier removal returns current water output to 5000", "water.water_production==5000 and water.water.production==5000")
    check("normal modifier removal clears container entry", "UIColony.label_modifiers.UndergroundWaterExtractor[effect]==nil")
    print(f"RESULT {count} controls passed; offline Lua only, no retail or save persistence measurement")


if __name__ == "__main__":
    main()
