#!/usr/bin/env python3
"""Wildfire: exercise shipped reveal, lock, research and legacy migration bodies.

Synthetic players; no retail game or reporter save. Class flattening, scheduler,
presentation and effect sinks are shims. Lock/prerequisite/research decisions
come from shipped Lua. Economy refunds are outside this availability experiment.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

import deskbench as db


def install(rt, rel, pattern, tree="1.1.0"):
    source, lo, hi = db.body(rel, pattern, tree)
    db.load_at(rt, source, "=" + rel, lo)
    print(f"SOURCE {tree} {rel}:{lo}-{hi} sha256={hashlib.sha256(source.encode()).hexdigest()}")


def main():
    print("COMMAND python tools/desk_wildfire_cure.py")
    print("HEAD " + subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=db.REPO, text=True).strip())
    bench = db.Bench("Wildfire availability: synthetic state, shipped decisions")
    rt = db.lua_runtime()
    rt.execute(db.ENGINE_SHIMS + r'''
        local native_next = next
        function next(t, k) if not t then return nil end return native_next(t, k) end
        function sorted_pairs(t) return pairs(t) end -- order irrelevant: one lock text
        function T(_, text) return text end
        function point(...) return {...} end
        function set(...) return {...} end
        function RGB(...) return 0 end
        function ObjModified() end
        function GetDialog() end
        function NotifyTechDiscovered() end
        function CountResearchedTech() end
        function LogResearchedTech() end
        function IsTechDiscounted() return false end -- excludes RP refunds, not tech spending
        function procall(fn, ...) if fn then return fn(...) end end
        function UnlockCrop(id) unlocked_crop = id end
        function GetDefaultResearchQueue() return UIPlayer end
        function table.findfirst(t, fn, ...)
            for i, v in ipairs(t) do if fn(i, v, ...) then return i, v end end
        end
        function table.find(t, value)
            for i, v in ipairs(t) do if v == value then return i end end
        end
        function table.common_keys(a, b)
            for k in pairs(a) do if b[k] ~= nil then return true end end
        end
        local handlers = {}
        message_handlers = handlers
        OnMsg = setmetatable({}, {__newindex = function(_, key, fn)
            handlers[key] = handlers[key] or {}; table.insert(handlers[key], fn)
        end})
        function Msg(name, ...) for _, fn in ipairs(handlers[name]) do fn(...) end end
        deferred = {}
        function DelayedCall(_, fn) table.insert(deferred, fn) end
        function CreateGameTimeThread(fn) table.insert(deferred, fn) end
        function drain()
            local iterations = 0
            while #deferred > 0 do
                local q = deferred; deferred = {}
                for _, fn in ipairs(q) do fn() end
                iterations = iterations + 1; assert(iterations < 100)
            end
        end
        function WaitMsg(name) coroutine.yield(name) end
        DefineClass = setmetatable({}, {__newindex = function(t, name, cls)
            for _, prop in ipairs(cls.properties) do cls[prop.id] = prop.default end
            setmetatable(cls, {__index = function(_, key)
                for _, parent in ipairs(cls.__parents) do
                    local p = _G[parent]; if p and p[key] ~= nil then return p[key] end
                end
            end})
            cls.class = name; rawset(t, name, cls); _G[name] = cls
        end})
        function IsKindOf(obj, name)
            if not obj then return false end
            if obj.class == name then return true end
            if obj.class == 'Tech' then return name == 'Preset' or name == 'LockablePreset' end
            return false
        end
        function ClassDescendantsList(name) assert(name == 'LockablePreset'); return {'Tech'} end
        Presets = {Tech = {}}; Techs = {}; SavegameFixups = {}
        Research = {}; ResearchQueue = {}; Player = {class = 'Player'}
        SA_RevealTech = {}; SA_GrantTechBoost = {}; SA_WaitResearch = {}
        const = {TechPointResearchCost = 1}; g_TechTimesResearched = {}
        g_ForceTechRepeatable = false; g_TechUnlockedCount = 0
    ''')
    rel = "CommonLua/Features/LockablePreset.lua"
    source = db.read(Path(db.SRC_LIVE) / rel)
    source = source[:source.index('\nDefineConstInt("Gameplay"')]
    db.load_at(rt, source, "=" + rel)
    print(f"SOURCE {rel}:1-{len(source.splitlines())} sha256={hashlib.sha256(source.encode()).hexdigest()}")
    rt.execute(r'''
        Tech = setmetatable({class = 'Tech', CanBeResearched = true,
            StartingNode = false, RequireTech = {}, Repeatable = false,
            EffectsApply = function(self)
                for _, effect in ipairs(self) do
                    if effect.OnApplyEffect then effect:OnApplyEffect(UIColony, self) end
                end
            end}, {__index = LockablePreset})
        g_Classes = {Tech = Tech}
        function PlaceObj(class, props, children)
            props = props or {}
            if class == 'TechTreeConnection' then
                local fields = {}
                for i = 1, #props, 2 do fields[props[i]] = props[i+1] end
                return fields
            end
            if class == 'Tech' then
                setmetatable(props, {__index = Tech}); Techs[props.id] = props
                local group = Presets.Tech[props.group] or {}; Presets.Tech[props.group] = group
                group[#group + 1] = props; group[props.id] = props
            end
            return props
        end
        function ForEachPreset(class, fn, ...)
            for group, list in pairs(Presets[class]) do
                for _, p in ipairs(list) do fn(p, group, ...) end
            end
        end
        function ResearchQueue:DequeueTech(id) table.remove_entry(self.tech_queue, id) end
        function Player:SetTechNew() end -- notification bookkeeping
        function Player:OnResetLockablePresetState() end
    ''')
    rel = "Data/Tech.lua"
    source = db.read(Path(db.SRC_LIVE) / rel)
    db.load_at(rt, source, "=" + rel)
    print(f"REGISTRY {rel} sha256={hashlib.sha256(source.encode()).hexdigest()}")
    rt.execute(r'''
        -- Restrict the lock-owner fixture to the family under test. Other techs
        -- have compiled script prerequisites that this class shim cannot build.
        Presets.Tech = {Mysteries = {}}
        for id, tech in pairs(Techs) do
            if id == 'WildfireCure' or id:match('^WildfireCure_%d+$') then
                assert(not tech.ShowPrerequisites and not tech.UnlockPrerequisites)
                table.insert(Presets.Tech.Mysteries, tech)
            end
        end
        assert(#Presets.Tech.Mysteries == 11)
    ''')
    common = "CommonLua/Libs/Research/Research.lua"
    for name in ("RemoveTechLockReason", "GetDefaultResearchQueue", "UnhideTech", "UnlockTech", "ResearchTech", "IsResearched", "GetTechState", "ResearchQueue:ResearchTech", "ResearchQueue:IsTechResearched"):
        install(rt, common, rf"^function {name}\(")
    rt.execute("baseUnlockTech = UnlockTech")
    tree = "Lua/TechTree.lua"
    for name in ("Tech:IsVisibleOnMap", "Tech:CheckUnlockPrerequisites", "Tech:ShouldCheckConditions", "IsConnectionVisible", "IsInitiative", "Player:CanResearch", "Player:IsTechResearched", "IsResearchQueueEntryAResearch", "Player:UIResearch", "UnhideUnlockedTechs", "UnlockTech", "SavegameFixups.TechPoints_MigrateDiscoveredSpecialTechs", "UnresearchAll"):
        install(rt, tree, rf"^function {name}\(")
    install(rt, "CommonLua/X/XPresetMap.lua", r"^function GetObjConnnectedTo\(")
    for name in ("IsTechUnlocked", "IsTechResearched", "IsTechRepeatable"):
        install(rt, "Lua/Tech.lua", rf"^function {name}\(")
    for name in ("Research:SetTechDiscovered", "Research:SetTechResearched", "Research:IsTechUnlocked", "Research:IsTechResearched", "Research:IsTechRepeatable", "Research:UpdateTechProgress", "Research:ChangeResearchCost", "Research:BoostTech", "BoostTech"):
        install(rt, "Lua/Research.lua", rf"^function {name}\(")
    source = db.read(Path(db.SRC_LIVE) / "Lua/Sequences/SA_Gameplay.lua")
    mapping = source[source.index("MysteryTechRevealRemapping = {"):source.index("function SA_RevealTech:SAExec()")]
    rt.execute(mapping)
    for name in ("SA_RevealTech:SAExec", "SA_GrantTechBoost:SAExec", "SA_WaitResearch:SAExec"):
        install(rt, "Lua/Sequences/SA_Gameplay.lua", rf"^function {name}\(")
    # Preserve the legacy field from the shipped creator, rather than infer it
    # from the scenario's editor-only Field='Special'.
    rt.execute("LegacyResearch = Research; Research = {}")
    install(rt, "Lua/Research.lua", r"^function Research:AddTech\(", "1.0.7")
    rt.execute("OldAddTech = Research.AddTech; Research = LegacyResearch")
    rt.execute(r'''
        setmetatable(Player, {__index = ResearchQueue})
        function fresh(points)
            deferred = {}; ConnectionStates = false
            UIPlayer = setmetatable({TechPoints = points, tech_researched = {},
                tech_research_points = {}, tech_queue = {}}, {__index = Player})
            Players = {UIPlayer}
            UIColony = setmetatable({mystery_id = 'TheMarsBug', tech_status = {}, TechBoostPerTech = {},
                TechBoostPerField = {}}, {__index = Research})
            PreProcessLockablePresets('init'); drain()
        end
        -- Same delayed unhide and immediate prerequisite checks as shipped handlers;
        -- UI refresh and compatibility notification consumers are presentation sinks.
        OnMsg.TechUnlocked = function() CheckLockPrerequisites(UIPlayer); DelayedCall(1, UnhideUnlockedTechs) end
        OnMsg.TechResearched = function() DelayedCall(1, UnhideUnlockedTechs) end
        OnMsg.LockablePresetsStateInit = UnhideUnlockedTechs
        OnMsg.PostLoadGame = UnhideUnlockedTechs
        function reveal() SA_RevealTech.SAExec{tech = 'WildfireCure', cost = 90000}; drain() end
        function boost() SA_GrantTechBoost.SAExec{Research = 'WildfireCure', Amount = 5, Update = true}; drain() end
        function hidden_family()
            for i = 1, 10 do if GetTechState('WildfireCure_' .. i) ~= 'hidden' then return false end end
            return GetTechState('WildfireCure') == 'hidden'
        end
    ''')
    def check(label, expr):
        bench.check(label, rt.eval(expr))

    rt.execute("fresh(11)")
    check("before reveal the entire cure family is hidden", "hidden_family()")
    rt.execute("reveal()")
    check("reveal makes chain head visible and purchasable", "GetTechState('WildfireCure_1') == 'enabled' and Techs.WildfireCure_1:IsVisibleOnMap() and UIPlayer:CanResearch('WildfireCure_1')")
    rt.execute("for i = 1, 10 do local id = 'WildfireCure_' .. i; assert(UIPlayer:UIResearch(id), id .. ':' .. tostring(GetTechState(id))); drain() end")
    check("normal research opens final cure", "UIPlayer.TechPoints == 1 and UIPlayer:CanResearch('WildfireCure')")
    rt.execute("assert(UIPlayer:UIResearch('WildfireCure')); drain()")
    check("final cure completes and invokes its crop effect", "IsTechResearched('WildfireCure') and unlocked_crop == 'Cure'")
    rt.execute("fresh(0); reveal()")
    check("zero points means visible but unaffordable", "Techs.WildfireCure_1:IsVisibleOnMap() and not UIPlayer:CanResearch('WildfireCure_1')")
    rt.execute("for i = 1, 10 do boost() end")
    check("medical advances all intermediates without tech points", "IsTechResearched('WildfireCure_10') and UIPlayer.TechPoints == 0 and GetTechState('WildfireCure') == 'enabled'")
    check("medical advancement leaves final cure requiring a point", "not IsTechResearched('WildfireCure') and not UIPlayer:CanResearch('WildfireCure')")
    rt.execute("UIPlayer.TechPoints = 1; assert(UIPlayer:UIResearch('WildfireCure')); drain(); SA_WaitResearch.SAExec{Field = 'Special', Research = 'WildfireCure', State = 'Researched'}")
    check("Field=Special does not block the completed cure wait", "IsTechResearched('WildfireCure')")
    rt.execute(r'''
        fresh(11)
        TechDef = {WildfireCure = {group = 'Mysteries'}}
        OldAddTech(UIColony, 'WildfireCure'); UIColony.tech_status.WildfireCure.discovered = 1
        SavegameFixups.TechPoints_MigrateDiscoveredSpecialTechs(); drain()
    ''')
    check("legacy field comes from Mysteries, not editor Field", "UIColony.tech_status.WildfireCure.field == 'Mysteries'")
    check("migration loses legacy revealed cure despite sufficient points", "hidden_family() and not UIPlayer:CanResearch('WildfireCure_1')")
    rt.execute("Msg('PostLoadGame'); drain()")
    check("post-load prerequisite sweep cannot reopen that family", "hidden_family()")
    rt.execute("boost()")
    check("a remaining medical advancement can reopen the migrated chain", "IsTechResearched('WildfireCure_1') and UIPlayer:CanResearch('WildfireCure_2')")
    rt.execute(r'''
        fresh(11)
        local control
        for id, tech in pairs(Techs) do
            if tech.group == 'Breakthroughs' and tech.LockState == 'hidden'
                and not tech.ShowPrerequisites and not tech.UnlockPrerequisites then
                control = tech; break
            end
        end
        assert(control)
        print('CONTROL migrated breakthrough ' .. control.id)
        ResetLockablePresetState(control, UIPlayer)
        assert(GetTechState(control.id) == 'hidden')
        UIColony.tech_status[control.id] = {field = 'Breakthroughs', discovered = 1}
        SavegameFixups.TechPoints_MigrateDiscoveredSpecialTechs(); drain()
        control_migrated = GetTechState(control.id) == 'enabled'
    ''')
    check("positive control: the same migrator restores a breakthrough", "control_migrated")
    # Load the actual module and core decision helpers. Register is the small
    # apply/veto driver only; WhenActive and Require are extracted unchanged.
    rt.execute(r'''
        SMRFixPack = {fixes = {}}
        function log() end
        function find_declaring_ancestor() end -- diagnostics only on a failed shape check
        function SMRFixPack.Log() repair_logs = (repair_logs or 0) + 1 end
        function SMRFixPack.Register(id, def)
            module_def = def
            local entry = {}; SMRFixPack.fixes[id] = entry
            if SMRFixPack_Disabled and SMRFixPack_Disabled[id] then entry.status = 'disabled'; return end
            local ok, why = pcall(def.apply)
            entry.status = not ok and 'error' or type(why) == 'string' and 'inactive' or 'active'
            entry.detail = why
        end
    ''')
    core = db.read(Path(db.REPO) / "Code/00_Core.lua").splitlines()
    for name in ("Require", "WhenActive"):
        hits = db.find_bodies(core, rf"^function SMRFixPack.{name}\(")
        assert len(hits) == 1
        lo, hi = hits[0]
        db.load_at(rt, '\n'.join(core[lo:hi+1]), "=Code/00_Core.lua", lo+1)
    module = db.read(Path(db.REPO) / "Code/Fix_WildfireCureMigration.lua")
    rt.execute("saved_colony = UIColony; saved_player = UIPlayer; saved_techs = Techs; UIColony = nil; UIPlayer = nil; Techs = nil")
    db.load_at(rt, module, "=Code/Fix_WildfireCureMigration.lua")
    check("cold-menu apply succeeds with no game or presets", "SMRFixPack.fixes.WildfireCureMigration.status == 'active'")
    rt.execute("UIColony = saved_colony; UIPlayer = saved_player; Techs = saved_techs")
    check("enable-path apply also succeeds with presets present", "module_def.apply() == nil")
    rt.execute(r'''
        function legacy()
            fresh(11); repair_logs = 0
            TechDef = {WildfireCure = {group = 'Mysteries'}}
            OldAddTech(UIColony, 'WildfireCure')
            UIColony.tech_status.WildfireCure.discovered = 1
            -- Already converted and still stuck: vanilla migration has run.
            SavegameFixups.TechPoints_MigrateDiscoveredSpecialTechs(); drain()
        end
        legacy()
        local_wait = coroutine.create(function()
            SA_WaitResearch.SAExec{Field = 'Special', Research = 'WildfireCure', State = 'Researched'}
            wait_finished = true
        end)
        assert(coroutine.resume(local_wait)); assert(coroutine.status(local_wait) == 'suspended')
        OnMsg.TechResearched = function()
            if local_wait and coroutine.status(local_wait) == 'suspended' then
                assert(coroutine.resume(local_wait))
            end
        end
        Msg('PostLoadGame'); drain()
    ''')
    check("already converted save recovers its research entrance on load", "UIPlayer:CanResearch('WildfireCure_1') and repair_logs == 1")
    check("repair grants no points, research or scenario completion", "UIPlayer.TechPoints == 11 and not IsTechResearched('WildfireCure_1') and not wait_finished and GetTechState('WildfireCure_2') == 'hidden'")
    rt.execute("Msg('PostLoadGame'); drain()")
    check("second load is idempotent", "repair_logs == 1 and UIPlayer:CanResearch('WildfireCure_1')")
    rt.execute(r'''
        -- Simulate another load with the mod disabled. Keep the actual vanilla
        -- saved lock tables and processed-preset markers; no engine serialization
        -- is claimed by this desk-only persistence check.
        SMRFixPack_Disabled = {WildfireCureMigration = true}
        Msg('PostLoadGame'); drain()
    ''')
    check("vanilla next-load processing preserves recovery with fix disabled", "UIPlayer:CanResearch('WildfireCure_1') and repair_logs == 1")
    rt.execute("SMRFixPack_Disabled = nil; for i = 1, 10 do assert(UIPlayer:UIResearch('WildfireCure_' .. i)); drain() end; assert(UIPlayer:UIResearch('WildfireCure')); drain()")
    check("recovered save reaches final research and releases existing wait", "wait_finished and IsTechResearched('WildfireCure') and UIPlayer.TechPoints == 0")
    rt.execute("Msg('PostLoadGame'); drain()")
    check("completed chain remains untouched", "repair_logs == 1 and IsTechResearched('WildfireCure')")
    for label, setup in (
        ("fresh unrevealed colony", "fresh(11); repair_logs = 0"),
        ("legacy undiscovered cure", "legacy(); UIColony.tech_status.WildfireCure.discovered = nil"),
        ("zero discovery marker", "legacy(); UIColony.tech_status.WildfireCure.discovered = 0"),
        ("foreign mystery", "legacy(); UIColony.mystery_id = 'MarsGateMystery'"),
        ("foreign saved field", "legacy(); UIColony.tech_status.WildfireCure.field = 'Storybits'"),
        ("changed reveal mapping", "legacy(); MysteryTechRevealRemapping.WildfireCure = 'WildfireCure_2'"),
        ("explicit veto", "legacy(); SMRFixPack_Disabled = {WildfireCureMigration = true}"),
        ("inactive registry", "legacy(); SMRFixPack.fixes.WildfireCureMigration.status = 'inactive'"),
    ):
        rt.execute(setup + "; Msg('PostLoadGame'); drain()")
        check("no mutation: " + label, "hidden_family() and repair_logs == 0")
        rt.execute("SMRFixPack_Disabled = nil; SMRFixPack.fixes.WildfireCureMigration.status = 'active'; MysteryTechRevealRemapping.WildfireCure = 'WildfireCure_1'")
    rt.execute("legacy(); reveal(); assert(UIPlayer:UIResearch('WildfireCure_1')); drain(); Msg('PostLoadGame'); drain()")
    check("partial progress is preserved without an extra reveal", "IsTechResearched('WildfireCure_1') and UIPlayer.TechPoints == 10 and repair_logs == 0")
    rt.execute(r'''
        legacy()
        for _, preset in ipairs(Presets.Tech.Mysteries) do
            UIPlayer.ProcessedLockablePresets[preset] = nil
        end
        UIPlayer.PresetLockStates = {}
        local callbacks = message_handlers.PostLoadGame
        callbacks[#callbacks]() -- recovery before vanilla's preset initialisation
        Msg('PostLoadGame'); drain()
    ''')
    check("new preset initialisation cannot re-hide an early recovery", "repair_logs == 1 and UIPlayer:CanResearch('WildfireCure_1')")
    rt.execute("legacy(); UnlockTech('WildfireCure', UIPlayer); drain(); Msg('PostLoadGame'); drain()")
    check("vanilla or external recovery stands the repair down", "GetTechState('WildfireCure') == 'enabled' and repair_logs == 0")
    rt.execute("saved_reader = GetPresetLockStateAndText; GetPresetLockStateAndText = function() return 'enabled' end")
    check("changed lock semantics decline the behaviour probe", "type(module_def.apply()) == 'string'")
    rt.execute("GetPresetLockStateAndText = function() error('unknown reader') end")
    check("unknown/throwing lock semantics decline", "type(module_def.apply()) == 'string'")
    rt.execute("GetPresetLockStateAndText = saved_reader; saved_can = Player.CanResearch; Player.CanResearch = nil")
    check("missing modern research API declines", "type(module_def.apply()) == 'string'")
    rt.execute("Player.CanResearch = saved_can")
    # The Steam report is not explained by an ordinary pre-1.1 save conversion:
    # exercise the shipped platform gate, including the allowed non-Steam route.
    install(rt, "CommonLua/SavegameMetadata.lua", r"^function ValidateSaveMetadata\(")
    install(rt, "CommonLua/SavegameMetadata.lua", r"^function GameSpecificValidateSaveMetadata\(metadata,")
    install(rt, "CommonLua/SavegameMetadata.lua", r"^function GetMissingMods\(")
    cfg = db.read(Path(db.SRC_LIVE) / "Lua/Config/config.lua")
    config_lines = '\n'.join(line for line in cfg.splitlines() if line.startswith(("config.SupportedSavegameLuaRevision =", "config.OldSavegameBehavior =")))
    rt.execute(r'''
        config = {}; Platform = {steam = true, developer = false}
        terminal = {desktop = {}}
        function GetLoadingScreenDialog() end
        function GetErrorTitle(id) return id end
        function GetErrorText(id) return id end
        function WaitMessage() end
        function WaitMultiChoiceQuestion() offered_load_anyway = true; return 1 end
        function table.set(t, k, v) t = t or {}; t[k] = v; return t end
    ''')
    rt.execute(config_lines)
    check("Steam retail blocks the archived legacy save revision", "ValidateSaveMetadata({lua_revision = 396349, active_mods = {}}, nil, {}, false, false) == 'old version'")
    rt.execute("Platform.steam = false")
    rt.execute(config_lines)
    check("non-Steam retail permits explicitly accepting Load anyway", "ValidateSaveMetadata({lua_revision = 396349, active_mods = {}}, nil, {}, false, false) == nil and offered_load_anyway")
    return bench.finish()


if __name__ == "__main__":
    sys.exit(main())
