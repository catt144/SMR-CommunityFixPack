#!/usr/bin/env python3
"""1.1.1 retirement source controls and active pack-on/pack-off desk controls.

Bodies are read from archived build 1.1.1.405907. F122, F123 and F126 load the
actual pre-retirement module from git 16ff1aa, so their pack-on control remains
available after the working-tree module is deleted. The remaining checks are
SOURCE controls over their replacement and a named native consumer. This is not
a game run. C93's retail asset gate and F119's fixup-enrolment gate are settled
evidence and deliberately are not re-executed here.

F126 runs the archived notification constructor with only its class/UI services
stubbed. EF008's engine assertions report and continue, unlike stock Lua's
abort-on-assert behavior; that continuation is explicitly modeled below and is
therefore a desk-execution limit rather than an engine run.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deskbench as db  # noqa: E402
from luafn import find_bodies, read_lines  # noqa: E402


REV = "16ff1aa"
BUILD = "1.1.1.405907"
ROOT = Path(os.environ.get("SMR_SRCARCHIVE", r"B:\Dev\SMR\SMR-Shared\SMR-SrcArchive"))
SRC = ROOT / BUILD / "Src"


def source(rel):
    return (SRC / rel).read_bytes().decode("utf-8", "replace").replace("\r\n", "\n")


def body(rel, pattern):
    lines = read_lines(str(SRC / rel))
    hits = find_bodies(lines, pattern)
    assert len(hits) == 1, (rel, pattern, len(hits))
    start, end = hits[0]
    return "\n".join(lines[start:end + 1]), start + 1, end + 1


def load(rt, rel, pattern, spans):
    text, first, last = body(rel, pattern)
    db.load_at(rt, text, "=" + rel, first)
    spans.append("%s:%d-%d" % (rel, first, last))
    return text, first


PRELUDE = db.ENGINE_SHIMS + r'''
OnMsg = {}
SMRFixPack = { fixes = {}, specs = {} }
function SMRFixPack.Register(id, spec)
  SMRFixPack.fixes[id] = { status = "active" }
  SMRFixPack.specs[id] = spec
end
function SMRFixPack.Require() return nil end
function SMRFixPack.WhenActive(id, fn)
  return function(...)
    if SMRFixPack.fixes[id].status == "active" then return fn(...) end
  end
end
function SMRFixPack.SetGlobal(id, fn) _G[id] = fn return nil end
function SMRFixPack.Log() end
function activate(id)
  local err = SMRFixPack.specs[id].apply()
  if err then error(err) end
end
'''


def runtime(extra=""):
    rt = db.lua_runtime()
    rt.execute(PRELUDE + extra)
    return rt


def old(rt, name):
    rel = "Code/Fix_%s.lua" % name
    db.load_at(rt, db.git_show(db.REPO, REV, rel), "=%s:%s" % (REV, rel), 1)
    rt.execute("activate('%s')" % name)


def active_controls(bench, spans):
    dome_extra = r'''
Community = {}
const = { Scale = { Stat = 100 } }
g_Consts = { LowStatLevel = 2500 }
AVG = 0
GetAverageStat = function() return AVG end
Untranslated = function(v) return v end
'''
    native = runtime(dome_extra)
    dome_body, dome_line = load(native, "Lua/X/ColonyControlCenter.lua",
                                r"^function Community:UICommandCenterStatUpdate\(", spans)
    native.execute(r'''
empty = { labels = { Colonist = {} } }
populated = { labels = { Colonist = { {} } } }
empty_win = { idLabel = { SetText = function(self, v) self.value = v end } }
populated_win = { idLabel = { SetText = function(self, v) self.value = v end } }
Community.UICommandCenterStatUpdate(empty, empty_win, 'Comfort')
AVG = 1000
Community.UICommandCenterStatUpdate(populated, populated_win, 'Comfort')
''')
    bench.check("F122 pack-off native leaves an empty dome's zero unhighlighted",
                native.eval("not string.find(tostring(empty_win.idLabel.value), '<red>')"))
    bench.check("F122 native positive control highlights a populated low-stat dome",
                native.eval("string.find(tostring(populated_win.idLabel.value), '<red>10</red>') ~= nil"))
    pack_on = runtime(dome_extra)
    load(pack_on, "Lua/X/ColonyControlCenter.lua", r"^function Community:UICommandCenterStatUpdate\(", [])
    pack_on.execute("empty = { labels = { Colonist = {} } }; empty_win = { idLabel = { SetText = function(self,v) self.value=v end } }")
    old(pack_on, "DomeOverviewHighlight")
    pack_on.execute("Community.UICommandCenterStatUpdate(empty, empty_win, 'Comfort')")
    bench.check("F122 actual 16ff1aa module restores the red empty-dome regression",
                pack_on.eval("empty_win.idLabel.value == '<red>0</red>'"))
    mutant = dome_body.replace("#colonists > 0 and v <", "v <")
    assert mutant != dome_body
    mutant_rt = runtime(dome_extra)
    db.load_at(mutant_rt, mutant, "=mutant/Dome.lua", dome_line)
    mutant_rt.execute("empty = { labels = { Colonist = {} } }; empty_win = { idLabel = { SetText = function(self,v) self.value=v end } }; Community.UICommandCenterStatUpdate(empty, empty_win, 'Comfort')")
    bench.check("F122 guard-reverted mutant fails the empty-dome control",
                mutant_rt.eval("empty_win.idLabel.value == '<red>0</red>'"))

    gene_extra = r'''
Techs = { GeneSelection = { ResolveValue = function() return 100 end }, GeneForging = { ResolveValue = function() return 50 end } }
researched = { GeneSelection = false, GeneForging = false }
IsTechResearched = function(id) return researched[id] end
'''
    gene = runtime(gene_extra)
    gene_body, gene_line = load(gene, "Lua/Units/Colonist.lua", r"^function GetRareTraitChance\(", spans)
    gene.execute("researched.GeneForging=true; forging=GetRareTraitChance(); researched.GeneSelection=true; both=GetRareTraitChance()")
    bench.check("F123 pack-off native pays Gene Forging once", gene.globals().forging == 50)
    bench.check("F123 native positive control sums the two tech bonuses", gene.globals().both == 150)
    old_gene = runtime(gene_extra)
    load(old_gene, "Lua/Units/Colonist.lua", r"^function GetRareTraitChance\(", [])
    old(old_gene, "GeneForging")
    old_gene.execute("researched.GeneForging=true; paid=GetRareTraitChance()")
    bench.check("F123 actual 16ff1aa wrapper double-pays native Gene Forging", old_gene.globals().paid == 100)
    mutant = gene_body.replace('if IsTechResearched("GeneForging") then', 'if false then')
    assert mutant != gene_body
    mutant_gene = runtime(gene_extra)
    db.load_at(mutant_gene, mutant, "=mutant/Colonist.lua", gene_line)
    mutant_gene.execute("researched.GeneForging=true; paid=GetRareTraitChance()")
    bench.check("F123 GeneForging-term mutant fails the pack-off control", mutant_gene.globals().paid == 0)

    presets = source("Data/NotificationPreset.lua")
    old_presets = (ROOT / "1.1.0.403908" / "Src" / "Data/NotificationPreset.lua").read_text(encoding="utf-8")
    bench.check("F126 1.1.1 deletes FounderGainsTrait, with its 1.1.0 preset as positive control",
                "FounderGainsTrait" not in presets and "FounderGainsTrait" in old_presets)

    add_notification, add_line, add_last = body(
        "CommonLua/Libs/Notifications/Notifications.lua", r"^function AddNotification\(")
    spans.append("CommonLua/Libs/Notifications/Notifications.lua:%d-%d" %
                 (add_line, add_last))
    create_instance, create_line, create_last = body(
        "CommonLua/PropertyObject.lua", r"^function PropertyObject:CreateInstance\(")
    spans.append("CommonLua/PropertyObject.lua:%d-%d" % (create_line, create_last))

    def founder_runtime(add_body=add_notification):
        rt = runtime(r'''
TraitPresets = { PositiveTrait = { group = 'Positive' } }
Notifications = {}
ShowOnceNotifications = {}
ENGINE_ASSERTS = {}
PropertyObject = {}

-- EF008 engine model: assertions are reported and execution continues. Stock
-- Lua would abort here, so this is intentionally not an engine execution.
assert = function(condition, message)
  if not condition then ENGINE_ASSERTS[#ENGINE_ASSERTS + 1] = message or 'assertion failed' end
  return condition
end

append_tuple = function(dest, ...)
  for i = 1, select('#', ...) do dest[#dest + 1] = select(i, ...) end
end
procall = function(fn, ...) if fn then return fn(...) end end
UpdateNotificationThread = function() end
Msg = function() end
''')
        db.load_at(rt, create_instance, "=CommonLua/PropertyObject.lua", create_line)
        rt.execute(r'''
NotificationPreset = {
  id = '', class = 'NotificationPreset', Parent = '', PerMap = false,
  ShowOnce = false, Suppressable = false,
  CanAddNotification = function() return true end,
}
NotificationPreset.__index = NotificationPreset
NotificationPreset.CreateInstance = PropertyObject.CreateInstance

local valid = {
  id = 'ValidFounderTrait', class = 'ValidFounderTrait', Parent = '',
  PerMap = false, ShowOnce = false, Suppressable = false,
  CanAddNotification = function() return true end,
}
valid.__index = valid
valid.CreateInstance = PropertyObject.CreateInstance
NotificationPresets = { ValidFounderTrait = valid }

FindNotification = function(id)
  local by_id = Notifications[id]
  return by_id and by_id[1]
end
''')
        db.load_at(rt, add_body, "=CommonLua/Libs/Notifications/Notifications.lua", add_line)
        return rt

    native_founder = founder_runtime()
    native_founder.execute(r'''
if OnMsg.ColonistAddTrait then
  OnMsg.ColonistAddTrait({traits={Founder=true}}, 'PositiveTrait', false)
end
''')
    bench.check("F126 pack-off event has no handler or notification-constructor call",
                native_founder.eval("type(OnMsg.ColonistAddTrait) ~= 'function' and #Notifications == 0 and #ENGINE_ASSERTS == 0"))

    founder = founder_runtime()
    old(founder, "FounderTraitNotification")
    founder.execute("OnMsg.ColonistAddTrait({traits={Founder=true}}, 'PositiveTrait', false)")
    bench.check("F126 actual 16ff1aa handler reaches archived unknown-ID assertion then base fallback",
                founder.eval("ENGINE_ASSERTS[1] == 'Invalid notification id' and ENGINE_ASSERTS[2] == 'assertion failed' and #Notifications == 1 and Notifications.FounderGainsTrait[1].Instance == true and Notifications.FounderGainsTrait[1].id == '' and getmetatable(Notifications.FounderGainsTrait[1]) == NotificationPreset"))

    valid_founder = founder_runtime()
    valid_founder.execute("valid = AddNotification('ValidFounderTrait', { marker = true })")
    bench.check("F126 archived constructor positive control creates a valid preset instance",
                valid_founder.eval("#ENGINE_ASSERTS == 0 and #Notifications == 1 and valid.Instance == true and valid.id == 'ValidFounderTrait' and valid.class == 'ValidFounderTrait' and getmetatable(valid) == NotificationPresets.ValidFounderTrait and Notifications.ValidFounderTrait[1] == valid"))

    founder.execute("TraitPresets.PositiveTrait.group='Other'; OnMsg.ColonistAddTrait({traits={Founder=true}}, 'PositiveTrait', false)")
    bench.check("F126 trait-group negative control cannot create a second notification",
                founder.eval("#Notifications == 1 and #ENGINE_ASSERTS == 2"))

    weakened_add_notification = add_notification.replace(
        'assert(id == "" or def, "Invalid notification id")',
        'assert(true, "Invalid notification id")')
    assert weakened_add_notification != add_notification
    weakened_founder = founder_runtime(weakened_add_notification)
    old(weakened_founder, "FounderTraitNotification")
    weakened_founder.execute("OnMsg.ColonistAddTrait({traits={Founder=true}}, 'PositiveTrait', false)")
    bench.check("F126 scratch-weakened native unknown-ID guard loses its diagnostic",
                weakened_founder.eval("#ENGINE_ASSERTS == 1 and ENGINE_ASSERTS[1] == 'assertion failed' and #Notifications == 1 and Notifications.FounderGainsTrait[1].Instance == true and getmetatable(Notifications.FounderGainsTrait[1]) == NotificationPreset"))


def source_controls(bench, spans):
    law = source("Data/LawDef/LawDef-Efficiency.lua")
    lax = law[law.index('id = "Policy_BuildingCodesLax"'):law.index('id = "Policy_BuildingCodesStrict"')]
    strict = law[law.index('id = "Policy_BuildingCodesStrict"'):]
    bench.check("C88 SOURCE: both Building Codes handlers set maintenance without a prefab argument or return",
                'if from_prefab then return end' not in law
                and law.count('bld:SetModifier("maintenance_resource_amount"') >= 2)

    # Extract the two current preset handlers instead of recreating their logic.
    def current_law_handler(law_id):
        at = law.index('id = "' + law_id + '"')
        start = law.index('Handler = function', at)
        end = law.index('\t\t\tend,', start) + len('\t\t\tend,')
        return law[start:end], law[:start].count('\n') + 1

    def run_law(handler, first, active=True):
        rt = runtime(r'''
ActiveLaws = { Policy_BuildingCodesStrict = true }
IsKindOf = function(obj, kind) return obj.kind == kind end
bld = { kind = 'RequiresMaintenance', SetModifier = function(self, prop, id, amount, percent) self.writes = (self.writes or 0) + 1; self.percent = percent end }
law = { id = 'Policy_BuildingCodesStrict', GetParameterValue = function() return -30 end, display_name = 'Strict' }
''')
        if not active:
            rt.execute('ActiveLaws = {}')
        db.load_at(rt, 'HOLDER = { ' + handler + ' }', '=Data/LawDef/LawDef-Efficiency.lua', first)
        rt.execute('HOLDER.Handler(law, bld, nil, true)')
        return rt

    strict_handler, strict_line = current_law_handler('Policy_BuildingCodesStrict')
    law_on = run_law(strict_handler, strict_line)
    law_off = run_law(strict_handler, strict_line, active=False)
    bench.check("C88 native handler applies Strict maintenance to a prefab-shaped completion",
                law_on.eval('bld.writes == 1 and bld.percent == -30'))
    bench.check("C88 native inactive-law control makes no maintenance write",
                law_off.eval('bld.writes == nil'))
    broken_law = strict_handler.replace('bld:SetModifier', '-- scratch removed bld:SetModifier')
    assert broken_law != strict_handler
    bench.check("C88 scratch-broken native handler fails the prefab completion control",
                run_law(broken_law, strict_line).eval('bld.writes == nil'))

    tunnel, tunnel_line, _ = body("Lua/Buildings/Tunnel.lua", r"^function TunnelBase:AddPFTunnel\(")
    spans.append("Lua/Buildings/Tunnel.lua:AddPFTunnel")
    bench.check("F38 SOURCE: AddPFTunnel rejects either destroyed half before pf.AddTunnel", "self.destroyed or self.linked_obj.destroyed" in tunnel and "pf.AddTunnel" in tunnel)
    def run_tunnel(text, destroyed):
        rt = runtime(r'''
TunnelBase = {}
pf = { adds = 0, AddTunnel = function() pf.adds = pf.adds + 1 end }
IsValid = function(obj) return obj ~= nil and not obj.invalid end
pathfind = { { DefaultPass = 1 } }
const = { PassTileSize = 1 }
point = { Dist2D = function() return 10 end }
endpoint = { GetEntrancePos = function() return point, { point } end }
self = { linked_obj = endpoint, GetEntrancePos = function() return point, { point } end }
''')
        rt.execute('self.linked_obj.destroyed = ' + ('true' if destroyed else 'false'))
        db.load_at(rt, text, '=Lua/Buildings/Tunnel.lua', tunnel_line)
        rt.execute('TunnelBase.AddPFTunnel(self)')
        return rt
    bench.check("F38 native destroyed-linked-half control suppresses pf.AddTunnel",
                run_tunnel(tunnel, True).eval('pf.adds == 0'))
    bench.check("F38 native positive control adds a valid tunnel to pathfinding",
                run_tunnel(tunnel, False).eval('pf.adds == 1'))
    broken_tunnel = tunnel.replace(' or self.linked_obj.destroyed', '')
    assert broken_tunnel != tunnel
    bench.check("F38 scratch-broken linked-half guard adds the forbidden tunnel",
                run_tunnel(broken_tunnel, True).eval('pf.adds == 1'))

    city, city_line, _ = body("Lua/X/ColonyControlCenter.lua", r"^function City:GetColonyStatsButtons\(")
    spans.append("Lua/X/ColonyControlCenter.lua:GetColonyStatsButtons")
    bench.check("F19 SOURCE: graph-caption sum and consumed-series consumer agree", "GetConsumedByConsumptionYesterday(id) + resource_overview_obj:GetConsumedByMaintenanceYesterday(id)" in city and "ts_resource.produced, ts_resource.consumed" in city)
    caption_at = city.index('\t\t\t\tcaption = function()', city.index('ts_resource.stockpile'))
    caption_end = city.index('\t\t\t\tend,', caption_at) + len('\t\t\t\tend,')
    caption = city[caption_at:caption_end]
    def run_caption(text):
        rt = runtime(r'''
id = 'Metals'
const = { ResourceScale = 100 }
resource_overview_obj = {
  GetProducedYesterday = function() return 900 end,
  GetConsumedByConsumptionYesterday = function() return 300 end,
  GetConsumedByMaintenanceYesterday = function() return 200 end,
}
T = function(t) return t end
''')
        db.load_at(rt, 'HOLDER = { ' + text + ' }', '=Lua/X/ColonyControlCenter.lua', city_line + caption.count('\n'))
        rt.execute('caption_value = HOLDER.caption()')
        return rt
    bench.check("F19 native graph caption invokes both consumption accumulators",
                run_caption(caption).eval('caption_value.consumed == 5'))
    broken_caption = caption.replace(' + resource_overview_obj:GetConsumedByMaintenanceYesterday(id)', '')
    assert broken_caption != caption
    bench.check("F19 scratch-broken caption loses the maintenance portion",
                run_caption(broken_caption).eval('caption_value.consumed == 3'))

    enabled, _, _ = body("Lua/Mysteries/MirrorSphere.lua", r"^function MirrorSphereBuildingBase:IsActionEnabled\(")
    start, _, _ = body("Lua/Mysteries/MirrorSphere.lua", r"^function MirrorSphereBuildingBase:StartAction\(")
    spans.extend(["Lua/Mysteries/MirrorSphere.lua:IsActionEnabled", "Lua/Mysteries/MirrorSphere.lua:StartAction"])
    bench.check("F16 SOURCE: max-progress refusal remains while same-action cancellation precedes it", "self.progress >= max_progress" in enabled and start.index("self.action == action") < start.index("self:IsActionEnabled"))
    mirror = runtime(r'''
MirrorSphereBuildingBase = {}
max_progress = 1000
T = function(_, text) return text end
''')
    _, enabled_line = load(mirror, "Lua/Mysteries/MirrorSphere.lua", r"^function MirrorSphereBuildingBase:IsActionEnabled\(", [])
    mirror.execute("finished={action=false,completed={},progress=1000}; same={action='FeedPower',completed={},progress=1000}")
    bench.check("F16 native finished-site action test declines at max_progress",
                mirror.eval("select(1, MirrorSphereBuildingBase.IsActionEnabled(finished, 'FeedPower')) == false"))
    bench.check("F16 native same-action positive control retains cancellation",
                mirror.eval("select(2, MirrorSphereBuildingBase.IsActionEnabled(same, 'FeedPower')) == 'Cancel.'"))
    broken_enabled = enabled.replace('self.progress >= max_progress', 'false')
    assert broken_enabled != enabled
    broken_mirror = runtime(r'''MirrorSphereBuildingBase = {}; max_progress = 1000; T = function(_, text) return text end''')
    db.load_at(broken_mirror, broken_enabled, '=mutant/MirrorSphere.lua', enabled_line)
    broken_mirror.execute("finished={action=false,completed={},progress=1000,dbg_enable_all=true}")
    bench.check("F16 scratch-broken max-progress guard admits the completed-site action",
                broken_mirror.eval("MirrorSphereBuildingBase.IsActionEnabled(finished, 'FeedPower') == true"))

    night, _, _ = body("Lua/Units/Colonist.lua", r"^function Colonist:ShouldLeaveForWork\(")
    spans.append("Lua/Units/Colonist.lua:ShouldLeaveForWork")
    bench.check("F04 SOURCE: native work predicate uses a wrapping day window", "(UIColony.hour - workshift_start) % hours_per_day" in night and "since_start <= 3" in night)
    night_rt = runtime(r'''
Colonist = {}
const = { DefaultWorkshifts = { { 6, 14 }, { 14, 22 }, { 22, 6 } } }
hours_per_day = 24
UIColony = { hour = 0 }
''')
    load(night_rt, "Lua/Units/Colonist.lua", r"^function Colonist:ShouldLeaveForWork\(", [])
    night_rt.execute('worker={workplace=true, workplace_shift=3}')
    bench.check("F04 native midnight positive control sends the third shift to work",
                night_rt.eval('Colonist.ShouldLeaveForWork(worker) == true'))
    night_rt.execute('UIColony.hour=8')
    bench.check("F04 native off-window control rejects an unrelated hour",
                night_rt.eval('Colonist.ShouldLeaveForWork(worker) == false'))

    animals = source("Lua/Units/Animals.lua")
    bench.check("C93 SOURCE: both new save fixups rebuild pasture stockpile pools", "SharePastureStockpilePools2" in animals and "MoveOpenPasturePilesOffOrigin2" in animals and "RebuildPastureStockpilePool(pasture)" in animals)

    generated = source("Lua/BuildingTemplate/Sinkhole.generated.lua")
    sink = source("Data/BuildingTemplate/Sinkhole.lua")
    destroy, destroy_line, _ = body("Lua/Buildings/Building.lua", r"^function DestroyBuildingImmediate\(")
    spans.append("Lua/Buildings/Building.lua:DestroyBuildingImmediate")
    bench.check("F96 SOURCE: both Sinkhole definitions set indestructible and its consumer returns", "indestructible = true" in generated and "indestructible = true" in sink and "bld.indestructible then" in destroy)
    def run_destroy(text, indestructible):
        rt = runtime(r'''
IsValid = function() return true end
IsKindOf = function() return false end
AddObjectToNotification = function() error('destroy path reached') end
''')
        db.load_at(rt, text, '=Lua/Buildings/Building.lua', destroy_line)
        rt.execute('sink={destroyed=false,indestructible=' + ('true' if indestructible else 'false') + '}; DestroyBuildingImmediate(sink,{reason="meteor"})')
        return rt
    bench.check("F96 native destruction consumer returns for an indestructible Sinkhole",
                run_destroy(destroy, True).eval('sink.destroyed == false'))
    broken_destroy = destroy.replace(' or bld.indestructible', '')
    assert broken_destroy != destroy
    try:
        run_destroy(broken_destroy, True)
        broke_sink_guard = False
    except Exception:
        broke_sink_guard = True
    bench.check("F96 scratch-broken destruction guard reaches the destructive branch", broke_sink_guard)

    fuel, fuel_line, _ = body("Lua/UniversalRocket.lua", r"^function UniversalRocketBase:OnModifiableValueChanged\(")
    fixup, _, _ = body("Lua/RocketCompatibility.lua", r"^function SavegameFixups.ZZZ_UpdateRefuelRequests\(")
    spans.extend(["Lua/UniversalRocket.lua:OnModifiableValueChanged", "Lua/RocketCompatibility.lua:ZZZ_UpdateRefuelRequests"])
    bench.check("F119 SOURCE: landed cargo callback refreshes and the upgrade fixup covers non-player rockets", "self.cargo and self:IsRocketLanded()" in fuel and "not rocket:IsPlayerControlled()" in fixup and "rocket:UpdateCargoResourceRequests()" in fixup)
    def run_fuel(text, landed):
        rt = runtime(r'''UniversalRocketBase = {}''')
        db.load_at(rt, text, '=Lua/UniversalRocket.lua', fuel_line)
        rt.execute('rocket={cargo={},IsRocketLanded=function() return ' + ('true' if landed else 'false') + ' end,UpdateCargoResourceRequests=function(self) self.calls=(self.calls or 0)+1 end}; UniversalRocketBase.OnModifiableValueChanged(rocket,"FuelResourceAmount")')
        return rt
    bench.check("F119 native landed-cargo callback refreshes the request", run_fuel(fuel, True).eval('rocket.calls == 1'))
    bench.check("F119 native flying-rocket control does not refresh", run_fuel(fuel, False).eval('rocket.calls == nil'))
    broken_fuel = fuel.replace('self:IsRocketLanded()', 'false')
    assert broken_fuel != fuel
    bench.check("F119 scratch-broken landed test leaves the request stale", run_fuel(broken_fuel, True).eval('rocket.calls == nil'))

    unload, unload_line, _ = body("Lua/Units/Train.lua", r"^function Train:UnloadAll\(")
    transfer, _, _ = body("Lua/Units/Train.lua", r"^function Train:TransferCargo\(")
    spans.extend(["Lua/Units/Train.lua:UnloadAll", "Lua/Units/Train.lua:TransferCargo"])
    bench.check("F46 SOURCE: native unload honors IsResourceEnabled and its transfer consumer invokes it", "not station:IsResourceEnabled(res)" in unload and "self.assigned_resources = assigned" in unload and "self:UnloadAll()" in transfer)
    def run_unload(text):
        rt = runtime(r'''
Train = {}
table.copy = function(t) local c = {}; for k,v in pairs(t) do c[k]=v end; return c end
table.keys = function(t) local r = {}; for k in pairs(t) do r[#r+1]=k end; return r end
RequestUnassignUnit = function() end
unload_cargo = function(train, station, res, amount) train.unloaded=(train.unloaded or 0)+amount end
dest={handle=1,demand={Food={GetTargetAmount=function() return 5 end}}}
station={storable_resources={'Food'},demand=dest.demand,IsResourceEnabled=function() return false end}
train={current_station=station,stockpiled_amount={Food=3},assigned_resources={[dest]={Food=3}}}
''')
        db.load_at(rt, text, '=Lua/Units/Train.lua', unload_line)
        rt.execute('Train.UnloadAll(train)')
        return rt
    bench.check("F46 native disabled-resource control preserves the cargo assignment",
                run_unload(unload).eval('train.unloaded == nil and train.assigned_resources[dest].Food == 3'))
    broken_unload = unload.replace('not station:IsResourceEnabled(res)', 'false')
    assert broken_unload != unload
    bench.check("F46 scratch-broken enablement guard unloads the disabled cargo",
                run_unload(broken_unload).eval('train.unloaded == 3'))

    demolished, demolished_line, _ = body("Lua/Buildings/Station.lua", r"^function OnMsg\.BuildingDemolished\(")
    spans.append("Lua/Buildings/Station.lua:OnMsg.BuildingDemolished")
    bench.check("F64 SOURCE: native station-demolition handler calls Train:DestroySilent", 'train:DestroySilent("station", bld)' in demolished)
    def run_demolished(text):
        rt = runtime(r'''
OnMsg = {}
IsKindOf = function(obj, class) return class == 'Station' and obj.kind == 'Station' end
ripairs = function(t) local i=#t+1; return function() i=i-1; if i >= 1 then return i,t[i] end end end
station={kind='Station',city={labels={Train={}}},RemoveServicedRanges=function(self) self.ranges=true end,ReleaseServicedDomes=function(self) self.domes=true end}
train={current_station=station,DestroySilent=function(self,why,obj) self.why=why; self.obj=obj end}
station.city.labels.Train={train}
''')
        db.load_at(rt, text, '=Lua/Buildings/Station.lua', demolished_line)
        rt.execute('OnMsg.BuildingDemolished(station)')
        return rt
    bench.check("F64 native station-demolition consumer calls DestroySilent with station context",
                run_demolished(demolished).eval("train.why == 'station' and train.obj == station"))
    broken_demolished = demolished.replace('train:DestroySilent("station", bld)', 'DoneObject(train)')
    assert broken_demolished != demolished
    broken_void = runtime(r'''
OnMsg = {}; IsKindOf=function(obj,class) return class=='Station' and obj.kind=='Station' end
ripairs=function(t) local i=#t+1; return function() i=i-1; if i>=1 then return i,t[i] end end end
DoneObject=function(train) train.done=true end
station={kind='Station',city={labels={Train={}}},RemoveServicedRanges=function() end,ReleaseServicedDomes=function() end}
train={current_station=station,DestroySilent=function(self) self.silent=true end}; station.city.labels.Train={train}
''')
    db.load_at(broken_void, broken_demolished, '=mutant/Station.lua', demolished_line)
    broken_void.execute('OnMsg.BuildingDemolished(station)')
    bench.check("F64 scratch-broken consumer deletes rather than stores the train",
                broken_void.eval('train.done == true and train.silent == nil'))

    board, board_line, _ = body("Lua/Units/ColonistTransport.lua", r"^function Colonist:BoardVehicle\(")
    exit_body, _, _ = body("Lua/Units/ColonistTransport.lua", r"^function Colonist:ExitVehicle\(")
    spans.extend(["Lua/Units/ColonistTransport.lua:BoardVehicle", "Lua/Units/ColonistTransport.lua:ExitVehicle"])
    bench.check("F21 SOURCE: boarding restamps start_wait before ExitVehicle consumes it", "self.transport_ticket.start_wait = GameTime()" in board and "GameTime() - ticket.start_wait" in exit_body)
    def run_board(text):
        rt = runtime(r'''
Colonist = {}
IsKindOf = function(obj, class) return class == 'Station' and obj.kind == 'Station' end
GameTime = function() return 100 end
RebuildInfopanel = function() end
PrgAmbientLife = { VisitDefault = 1 }
const = { HourDuration = 1 }
station={kind='Station',AddSpentTime=function(self,value) self.spent=value end}
vehicle={IncreasePassengersCount=function() end,track={IncreasePassengersCount=function() end}}
colonist={holder=station,transport_ticket={start_wait=40,src_station={waiting_for_train={}}},
 PushDestructor=function(self,fn) self.destructor=fn end,
 PopAndCallDestructor=function(self) self.destructor(self) end,
 SetHolder=function(self,holder) self.holder=holder end,
 SetState=function() end, PlayPrg=function(self) self.holder=false end}
''')
        db.load_at(rt, text, '=Lua/Units/ColonistTransport.lua', board_line)
        rt.execute('Colonist.BoardVehicle(colonist,vehicle)')
        return rt
    bench.check("F21 native boarding records the platform wait and restamps the ride boundary",
                run_board(board).eval('station.spent == 60 and colonist.transport_ticket.start_wait == 100'))
    broken_board = board.replace('self.transport_ticket.start_wait = GameTime()', '-- scratch removed restamp')
    assert broken_board != board
    bench.check("F21 scratch-broken boarding leaves the pre-boarding timestamp intact",
                run_board(broken_board).eval('colonist.transport_ticket.start_wait == 40'))

    wisp, wisp_line, _ = body("Lua/Mysteries/Fireflies.lua", r"^function SetLightTrapMode\(")
    spans.append("Lua/Mysteries/Fireflies.lua:SetLightTrapMode")
    bench.check("F07/F15 SOURCE: free mode scales power by 1000 and batch destroy has no research grant", "el_prod_modifier:Change(#trap.fireflies * 1000)" in wisp and "AddResearchPoints" not in wisp)
    def run_wisp(text):
        rt = runtime(r'''
UIColony={mystery={}}
MainCity={labels={LightTrap={}}}
AddUniqueNotification=function() end
PlayFX=function() end
modifier={Change=function(self,amount) self.amount=amount end}
trap={fireflies={{},{},{}},el_prod_modifier=modifier,UpdateAttachedSigns=function() end,SetWorkState=function() end}
MainCity.labels.LightTrap={trap}
''')
        db.load_at(rt, text, '=Lua/Mysteries/Fireflies.lua', wisp_line)
        rt.execute("SetLightTrapMode('free')")
        return rt
    bench.check("F07 native free-mode consumer turns three wisps into 3000 power units",
                run_wisp(wisp).eval('modifier.amount == 3000'))
    broken_wisp = wisp.replace('#trap.fireflies * 1000', '#trap.fireflies')
    assert broken_wisp != wisp
    bench.check("F07 scratch-broken free-mode multiplier exposes the three-unit payout",
                run_wisp(broken_wisp).eval('modifier.amount == 3'))
    def destroy_reward(text):
        rt = run_wisp(text)
        rt.execute(r'''
research = 0
AddResearchPoints = function(points) research = research + points end
for _, firefly in ipairs(trap.fireflies) do firefly.SetCommand = function() end end
SetLightTrapMode('destroy')
''')
        return rt
    bench.check("F15 native batch-destroy path leaves research to the per-wisp consumer",
                destroy_reward(wisp).eval('research == 0'))
    broken_reward = wisp.replace('AddUniqueNotification("Mystery11WispsKilled", {points = reward})',
                                 'AddResearchPoints(reward); AddUniqueNotification("Mystery11WispsKilled", {points = reward})')
    assert broken_reward != wisp
    bench.check("F15 scratch-broken batch grant double-pays the three-wisp reward",
                destroy_reward(broken_reward).eval('research == 300'))


def main():
    print("COMMAND python tools/desk_gamepatch_retirements.py")
    print("SOURCE %s" % SRC)
    print("PACK-ON MODULES %s" % REV)
    bench = db.Bench("1.1.1 retirements: native replacement/consumer source controls")
    spans = []
    active_controls(bench, spans)
    source_controls(bench, spans)
    print("\nEXTRACTED:")
    for span in spans:
        print("  " + span)
    return bench.finish("ALL DEMANDS HELD -- active modules regress the repaired path; native replacement and consumer controls hold.")


if __name__ == "__main__":
    raise SystemExit(main())
