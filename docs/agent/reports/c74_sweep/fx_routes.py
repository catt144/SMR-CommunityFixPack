"""Assign every non-generic-moment FX entry to a firing ROUTE (hand-traced, cited), then
emit candidate groups. Run after fx_census.py. Usage: python fx_routes.py [1.1.0|1.0.7]"""
import json, os, re, sys, collections
OUT = os.path.dirname(os.path.abspath(__file__))
tree = sys.argv[1] if len(sys.argv) > 1 else "1.1.0"
C = json.load(open(os.path.join(OUT, "census_%s.json" % tree)))
PRESET_GROUPS = set(a["group"] for a in C["animmeta"])

# route kinds:
#  CODE     = code call site fires this (Action, Moment) directly; cited
#  PRESET   = fired by an anim-moment reader that needs Presets.AnimMetadata[entity] (dead unless preset)
#  TRACKER  = BaseBuilding:TrackMultipleHitMoments (dead: index-vs-name + no preset)
#  NOPATH   = no code fires the moment for this Action even if every preset existed (unreachable)
#  DISABLED = entry Disabled=true (never plays)
R = [
 # (Action regex, Moment regex, kind, evidence, entity the anim must carry)
 (r"^ElectrostaticStorm$", r"^hit-moment[1-4]$", "CODE", "Lua/DustStorm.lua:267 'hit-moment'..(1+Random(4)), actor nil -> Actor any; _fixup.lua:1556 unpacks the table form", None),
 (r"^Dig$", r"^hit-moment\d$", "CODE", "Lua/Mysteries/MirrorSphere.lua:872-873 format('hit-moment%d', count(completed)) PlayFX('Dig',..,self)", None),
 (r"^StirlingGenerator$", r"^hit-moment$", "CODE", "Lua/Buildings/StirlingGenerator.lua:72 (fires even if TimeToMoment returns nil)", None),
 (r"^MysteryDream$", r"^hit-moment$", "CODE", "Lua/Units/Colonist.lua:4959+4965 StartFX('MysteryDream') then PlayFXMoment('hit-moment') -> Unit.lua:89-92 PlayFX(self.fx, moment, self)", None),
 (r"^Working$", r"^hit-moment[1-3]$", "TRACKER", "Lua/Buildings/BaseBuilding.lua:929/947 -> :1037 TrackMultipleHitMoments; :1046 GetAnimMomentsCount(GetAnim(1) index, 'Hit')", "tracked attach"),
 (r"^Working$", r"^hit-moment4$", "NOPATH", "tracker lists stop at 3 (MetalsExtractor.lua:25, BaseBuilding.lua:1026 stops at 2); nothing emits hit-moment4 for Working", None),
 (r"^MetatronRotation$", r"^End\d$", "PRESET", "Lua/Mysteries/Metatron.lua:51-80 own tracker, GetAnimMomentsCount(GetAnim(1) index, 'End') -> PlayFX('MetatronRotation', 'End'..i); also index-vs-name", "Monolith"),
 (r"^MetatronRotation$", r"^hit-moment\d$", "NOPATH", "Metatron.lua:57 tracks only 'Start'/'End' and emits moment..i ('Start1','End1'..); no code emits hit-moment<i> for MetatronRotation", None),
 (r"^Anim:workIdle$", r"^bread_", "PRESET", "DLC/norman/Code/Bakery.lua:1-4 BakeryHands AnimMomentHook anim_moments_hook_all -> AnimMomentHook.lua:127 WaitTrackMoments -> AnimMoment.lua:153 PlayFX(FXAnimToAction(anim), moment, self)", "BakeryHands"),
 (r"^Drill$", r"^Hit$", "PRESET", "Lua/Units/RCDriller.lua:105 TrackAllMoments(self,'Drill') -> Building.lua:3346-3369 GetAllAnimMoments -> presets", "RoverRussiaDriller"),
 (r"^ShuttleHubEnter$", r"^Hit$", "PRESET", "Lua/Buildings/ShuttleHub.lua:1632 TrackAllMoments(shuttle,'ShuttleHubEnter',shuttle,hub)", "shuttle entity"),
 (r"^ShuttleHubExit$", r"^Hit$", "PRESET", "Lua/Buildings/ShuttleHub.lua:1649 TrackAllMoments(shuttle,'ShuttleHubExit',shuttle,hub)", "shuttle entity"),
 (r"^working$", r"^Hit$", "PRESET", "Lua/Buildings/WaterExtractor.lua:115 TrackAllMoments(pump,'working',self)", "WaterExtractorPump"),
 (r"^ExcavatorDigging$", r"^(Hit|Out)\d+$", "PRESET", "Lua/Buildings/TheExcavator.lua:120 TrackAllMoments(self.arm,'ExcavatorDigging',self.arm)", "ExcavatorShovel"),
 (r"^(Construct|Load)$", r"^Hit1$", "PRESET", "Lua/Units/RCTransport.lua:133-134 TrackAllMoments(self, fx, self, building) when anim_idle in track_anim_moments (RCTerraformer.lua:35 {'workIdle'})", "RoverTerraformer"),
 (r"^ConstructingDrones$", r"^Hit\d$", "NOPATH", "only PlayFX('ConstructingDrones','start'/'end') exist (DroneFactory.lua:52/63, Station.lua:527/537); no tracker on DroneHub", None),
 (r"^HydroponicFarm$", r"^(Lift|Spray|Rotate)", "NOPATH", "no PlayFX('HydroponicFarm',..) anywhere; FarmHydroponic:StartAnimThread is empty (Farm.lua:1033; 1.0.7 Farm.lua:796); HydroponicFarmElevator is a bare BuildingEntityClass (Farm.lua:1036)", None),
 (r"^RegolithExtractorDigging$", r"^dig-reveerse$", "NOPATH", "typo of 'dig-reverse' (code emits 'dig-reverse' RegolithExtractor.lua:494/737)", None),
 (r"^CrystalCompose$", r"^attach\d+$", "CODE", "Lua/Mysteries/Crystals.lua:288 'attach'..#arrived", None),
 (r"^PlantsGrowing$", r"^idle\d$", "CODE", "Lua/Buildings/Farm.lua:411 PlayFX('PlantsGrowing', state, ...) with state from Crop.lua:19-20 sequences", None),
 (r"^EmergencyRecharge$", r"^hooking$", "CODE", "Lua/Buildings/RechargeStation.lua:179 / RCRover.lua:170 StartFX('EmergencyRecharge') then Drone.lua:1578 PlayFXMoment('hooking')", None),
 (r"^BlackCubeDemolishBuilding$", r"^hit$", "CODE", "Data/Scenario/Mystery 1.lua:414-415 SA_DestroyObjects fx_action/fx_moment -> SA_Gameplay.lua:2024", None),
 (r"^BuildingInteractableComponent$", r".", "DISABLED", "all entries Disabled", None),
]

def route(e):
    if e.get("Disabled"):
        return ("DISABLED", "Disabled=true", None)
    for ar, mr, kind, ev, ent in R:
        if re.search(ar, e["Action"]) and re.search(mr, e["Moment"]):
            return (kind, ev, ent)
    return (None, None, None)

TARGETS = {"hit-moment"}
rows = []
for e in C["fx"]:
    if e["class"] == "ActionFXRemove": continue
    k, ev, ent = route(e)
    if k:
        rows.append(dict(e, route=k, evidence=ev, anim_entity=ent))
json.dump(rows, open(os.path.join(OUT, "routes_%s.json" % tree), "w"), indent=0)

print("== routed entries", tree, collections.Counter(r["route"] for r in rows))
g = collections.defaultdict(list)
for r in rows:
    if r["route"] in ("PRESET", "TRACKER", "NOPATH"):
        g[(r["route"], r["Action"], r["Actor"], r["Target"], r["anim_entity"])].append(r)
for key, es in sorted(g.items(), key=lambda kv: (-len(kv[1]))):
    route_, a, act, tgt, ent = key
    has = (ent in PRESET_GROUPS) if ent else None
    print("  %-8s n=%-2d %s Actor=%s Target=%s anim_entity=%s preset=%s kinds=%s moments=%s sites=%s" % (
        route_, len(es), a, act, tgt, ent, has, dict(collections.Counter(x["class"][8:] for x in es)),
        sorted(set(x["Moment"] for x in es)), ",".join(x["file"].split("/")[-1].replace("ActionFX", "") + ":" + str(x["line"]) for x in es)))
